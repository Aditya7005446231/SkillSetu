import { useEffect } from 'react';
import { supabase } from './services/supabase';

function App() {
  useEffect(() => {
    async function testConnection() {
      const { data, error } = await supabase.auth.getSession();

      if (error) {
        console.error(error);
      } else {
        console.log("Supabase connected!", data);
      }
    }

    testConnection();
  }, []);

  return (
    <div>
      <h1>CareerBridge AI</h1>
      <p>Supabase connection test</p>
    </div>
  );
}

export default App;