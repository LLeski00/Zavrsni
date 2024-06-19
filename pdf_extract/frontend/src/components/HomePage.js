import React, {Component} from "react";
import { useState } from "react";

const HomePage = () => {

    let file;
    let formData = new FormData();
    const [studentData,setStudentData] = useState({});
    const [isLoading, setIsLoading] = useState(false);

    const handleButtonClick = () => {
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                votes_to_skip: 5,
                guest_can_pause: true
            })
        };
        fetch('/api/create-student', requestOptions)
        .then((response) => response.json())
        .then((data) => console.log(data));
    };

    const handleFileUpload = (event) => {
        file=event.target.files[0];
        formData.append('file',file);
    };

    const handleFileUploadClick = () => {
            setIsLoading(true);

            fetch('http://127.0.0.1:8000/api/extract', { // Your POST endpoint
              method: 'POST',
              body: formData // This is your file object
            }).then(
              response => response.json() // if the response is a JSON object
            ).then(
              success => {
                setStudentData(success);
                console.log(success);
                setIsLoading(false);
              } // Handle the success response object
            ).catch(
              error => console.log(error) // Handle the error response object
            );
    };

    return (
        <div className="HomePage">
            <div className="home-page-content">
                <h1>Test</h1>
                <button onClick={handleButtonClick}>Click</button>
                <input type="file" onChange={()=>handleFileUpload(event)}/>
                <button onClick={handleFileUploadClick}>Upload</button>
                {isLoading && <p>Loading...</p>}
                <p>{studentData.student_name}</p>
            </div>
        </div>
    );
}
 
export default HomePage;