import { useRef, useState } from 'react'
import { CheckCircle2, FileUp, LoaderCircle, UploadCloud, X } from 'lucide-react'
import { analyzeResume } from '../services/resume'

function ResumeUpload({ onAnalyzed }) {
  const inputRef = useRef(null)
  const [file, setFile] = useState(null)
  const [dragging, setDragging] = useState(false)
  const [status, setStatus] = useState('')
  const [error, setError] = useState('')

  function chooseFile(nextFile) {
    setError('')
    if (!nextFile) return
    if (nextFile.type !== 'application/pdf') {
      setError('Please choose a PDF resume.')
      return
    }
    if (nextFile.size > 5 * 1024 * 1024) {
      setError('Your resume must be smaller than 5 MB.')
      return
    }
    setFile(nextFile)
    setStatus('')
  }

  async function submit(event) {
    event.preventDefault()
    if (!file) return setError('Choose a resume before analyzing it.')
    setError('')
    setStatus('analyzing')
    try {
      const result = await analyzeResume(file)
      onAnalyzed(result.profile)
      setStatus('complete')
    } catch (requestError) {
      setStatus('')
      setError(requestError.response?.data?.detail || requestError.message || 'Resume analysis failed.')
    }
  }

  return (
    <form className="upload-card" onSubmit={submit}>
      <div className="card-title-row"><div><p className="eyebrow purple">RESUME INTELLIGENCE</p><h2>Upload your resume</h2><p className="muted">We will turn your experience into a clear skill profile.</p></div><div className="upload-icon"><UploadCloud size={21} /></div></div>
      <button type="button" className={`drop-zone ${dragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`} onClick={() => inputRef.current?.click()} onDragOver={(event) => { event.preventDefault(); setDragging(true) }} onDragLeave={() => setDragging(false)} onDrop={(event) => { event.preventDefault(); setDragging(false); chooseFile(event.dataTransfer.files[0]) }}>
        <input ref={inputRef} type="file" accept="application/pdf" hidden onChange={(event) => chooseFile(event.target.files[0])} />
        {file ? <><span className="file-icon"><FileUp size={19} /></span><strong>{file.name}</strong><small>{(file.size / 1024 / 1024).toFixed(2)} MB · Ready to analyze</small></> : <><span className="drop-icon"><UploadCloud size={23} /></span><strong>Drop your PDF here</strong><small>or click to browse · PDF up to 5 MB</small></>}
      </button>
      {file && <button type="button" className="remove-file" onClick={() => { setFile(null); setStatus('') }}><X size={14} /> Remove file</button>}
      {error && <p className="form-error">{error}</p>}
      {status === 'complete' && <p className="form-success"><CheckCircle2 size={15} /> Profile analyzed and saved to your account.</p>}
      <button className="analyze-button" type="submit" disabled={!file || status === 'analyzing'}>{status === 'analyzing' ? <><LoaderCircle className="spin" size={17} /> Reading your resume...</> : 'Analyze my resume →'}</button>
    </form>
  )
}

export default ResumeUpload
