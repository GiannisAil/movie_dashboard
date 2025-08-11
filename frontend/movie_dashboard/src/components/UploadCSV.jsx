import {useState} from 'react';

export default function UploadCSV(){

    const [file, setFile] = useState(null);
    const onFileChange = (event) => {
        setFile(event.target.files[0]);
    }

    const onFileUpload = () => {
        return null;
    }

    return (
        <div>
            <h1>Upload your Letterboxd watched.csv file</h1>
            <input type="file" accept=".csv" id='selectedFile' style={{display: 'none'}} onChange={onFileChange}/>
            <input type="button" value="Choose File" onClick={() => document.getElementById('selectedFile').click()} />
            { file && (
                <div>
                    <h2>File Selected: {file.name}</h2>
                    <button onClick={onFileUpload}>Get Your Stats!</button>
                </div>
            )}
        </div>
    )
}