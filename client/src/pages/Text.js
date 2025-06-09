import React, { useRef, useState } from 'react';
import axios from 'axios';
import "../css/Text.css";

export default function Text() {
    const fileInputRef = useRef(null);
    const [tokens, setTokens] = useState(null);
    const [isLoading, setIsLoading] = useState(false); 

    const handleUploadClick = () => {
        fileInputRef.current.click();
    };

    const handleFileChange = async (event) => {
        const file = event.target.files[0];
        if (file) {
            const allowedTypes = ["application/pdf"];
            if (allowedTypes.includes(file.type)) {
                alert(`You uploaded the file: ${file.name}`);
                setIsLoading(true); 
                const formData = new FormData();
                formData.append("file", file);
                try {
                    const response = await axios.post("http://localhost:5000/text/collect_data", formData);

                    setTokens(response.data);
                    setIsLoading(false);
                } catch (error) {
                    alert("Error analyzing the file.");
                    setIsLoading(false);
                }
            } else {
                alert("Please upload only one PDF file!");
                event.target.value = null;
            }
        }
    };

    return (
        <div className="page-container">
            <div className="content-box">
                <p>Dear user, please upload PDF file:</p>
                <div className="input-wrapper">
                    <button className="upload-button" onClick={handleUploadClick}>
                        📎
                    </button>
                    <input
                        type="file"
                        ref={fileInputRef}
                        accept=".pdf"
                        hidden  
                        onChange={handleFileChange}
                    />
                </div>
                {isLoading && (
                    <div className="loading-container">
                        <div className="bouncing-dots">
                            <span>.</span><span>.</span><span>.</span>
                        </div>
                        <p className="loading-text">Your document? We're already in the middle of the story...</p>
                    </div>
                )}
    
    {tokens && (
  <div>
    <h2>Predicted Author: {tokens.label}</h2>
    <h3>Probabilities:</h3>
    <ul>
      {Object.entries(tokens.probabilities).map(([author, prob]) => (
        <li key={author}>
          {author}: {(prob * 100).toFixed(2)}%
        </li>
      ))}
    </ul>
  </div>
)}

            </div>
        </div>
    );
}    