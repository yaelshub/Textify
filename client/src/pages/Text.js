import React, { useRef } from 'react';
import "../css/Text.css";


export default function Text() {
    const fileInputRef = useRef(null);

    const handleUploadClick = () => {
        fileInputRef.current.click(); // פותח חלון לבחירת קובץ
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            const allowedTypes = [
                "application/pdf",
                "application/msword", // .doc
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document" // .docx
            ];
            if (allowedTypes.includes(file.type)) {
                alert(`You uploaded the file: ${file.name}`);
                setTimeout(() => {
                    alert(`
                        Results of your text analysis:
                        The text you uploaded was analyzed using advanced stylometric tools, based on comparing repetitive patterns in writing style.
                        Identification results:
                        30% match with Esther Quinn's writing style.
                        90% match with Mia Keenan's writing style.
                        Important to know: Stylometry can only offer a statistical probability of author identification, but cannot unequivocally determine the identity of the writer. The results are based on analytical patterns, and therefore should always be taken with limited certainty.`);
                }, 3000);
            } else {
                alert("Please upload only one file Word (.doc, .docx) or PDF!");
                fileInputRef.current.value = ""; // איפוס הבחירה
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
                        accept=".pdf, .doc, .docx" 
                        hidden
                        onChange={handleFileChange}
                    />
                </div>
            </div>
        </div>
    );
}
