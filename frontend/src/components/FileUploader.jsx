import { useState } from "react";
import "../App.css";
const FileUploader = ({onUpload}) => {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState("");

  const handleUpload = async () => {
    const API = import.meta.env.VITE_API_URL;

    try{
      if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
     //const authToken = localStorage.getItem('authToken');

    const response = await fetch(`${API}/upload_file`, {
      method: "POST",
      body: formData,
      /*headers: {
        'Authorization': `Bearer ${authToken}`,
      }*/
    });
    if (!response.ok) {
     
      const errText = await response.text(); 
      console.error('Upload failed:', response.status, errText);
      return; 
    }
     const contentLength = response.headers.get('Content-Length');
    if (contentLength === '0' || contentLength === null) {
      console.log('Upload successful, but no JSON response body.');
      
      return;
    }
    const data = await response.json();
    console.log('Upload successful:', data);
    setResponse(data.narrative || "No narrative generated.");
    onUpload(data.narrative);

    }
    catch(err){
      console.error('Error during upload:', err); 
    }
    

    
  };

  return (
    <div className="card">
      <h1>NarratAIve AI Data Analyzer</h1>
      <input
        type="file"
        accept=".csv,.json"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button
        onClick={handleUpload}
        className="button"
      >
        Upload & Generate
      </button>

      {/*
      {response && (
        <div className="">
          {response}
        </div>
      )}
      */}
    </div>
  );
};

export default FileUploader;
