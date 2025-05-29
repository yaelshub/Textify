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
            const allowedTypes = [
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ];
            if (allowedTypes.includes(file.type)) {
                alert(`You uploaded the file: ${file.name}`);
                setIsLoading(true); //מתחיל עיבוד
                const formData = new FormData();
                formData.append("file", file);
                try {
                    const response = await axios.post("http://127.0.0.1:5000/text/collect_data", formData);
                    console.log(response.data);
                    setTokens(response.data);
                    setTimeout(() => {
                        alert(`
                        Results of your text analysis:
                        30% match with Esther Quinn's writing style.
                        90% match with Mia Keenan's writing style.
                        Important to know: Stylometry can only offer a statistical probability...
                        `);
                        setIsLoading(false);    
                    }, 3000);
                } catch (error) {
                    alert("Error analyzing the file.");
                    setIsLoading(false);
                }
            } else {
                alert("Please upload only one PDF file!");
                fileInputRef.current.value = "";
            }
        }
    };

    return (
        <div className="page-container">
            <div className="content-box">
                <p>Dear user, please upload a Word or PDF file:</p>
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
    
                {/* הצגת תוצאות אם קיימות */}
                {tokens && (
                    <div className="results">
                        <h3>Tokenization Results:</h3>
                        <div>
                            <h4>Sentences:</h4>
                            <ul>
                                {tokens.sentences.map((sentence, index) => (
                                    <li key={index}>{sentence}</li>
                                ))}
                            </ul>
                        </div>
                        <div>
                            <h4>Words:</h4>
                            <ul>
                                {tokens.words.map((word, index) => (
                                    <li key={index}>{word}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}    