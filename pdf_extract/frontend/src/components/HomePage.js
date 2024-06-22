import React, { Component, useEffect, useRef } from "react";
import { useState } from "react";

const HomePage = () => {
    const formData = useRef(new FormData());
    const [studentData, setStudentData] = useState(null);
    const [majorsData, setMajorsData] = useState(null);
    const [currentStudentMajor, setCurrentStudentMajor] = useState(null);
    const [futureStudentMajor, setFutureStudentMajor] = useState(null);
    const [currentStudentMajorId, setCurrentStudentMajorId] = useState(null);
    const [futureStudentMajorId, setFutureStudentMajorId] = useState(null);
    const [fileName, setFileName] = useState("");
    const [transferId, setTransferId] = useState("");
    const [requiredStudentSubjects, setRequiredStudentSubjects] =
        useState(null);
    const [recognizedStudentSubjects, setRecognizedStudentSubjects] =
        useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        fetchMajors();
    }, []);

    const fetchMajors = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/get-data`);
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const res = await response.json();
            await setMajorsData(res); // Assuming the API returns JSON
            console.log(res);
        } catch (error) {
            setError(error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCurrentMajorSelect = async (event) => {
        setCurrentStudentMajorId(event.target.value);
        setCurrentStudentMajor(await getSubjects(event.target.value));
        console.log(event.target.value);
    };

    const handleFutureMajorSelect = async (event) => {
        setFutureStudentMajorId(event.target.value);
        setFutureStudentMajor(await getSubjects(event.target.value));
        console.log(event.target.value);
    };

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        setFileName(file.name);
        formData.current.append("file", file);
    };

    const handleFileUploadClick = async () => {
        setIsLoading(true);
        if (!currentStudentMajor || !futureStudentMajor) {
            console.log(currentStudentMajor);
            console.log(futureStudentMajor);
            alert("Not enough data.");
            setIsLoading(false);
            return;
        }

        setTransferId(currentStudentMajorId + "-" + futureStudentMajorId);
        console.log("File uploaded: ", formData.current.get("file"));

        await fetch("http://127.0.0.1:8000/api/extract", {
            // Your POST endpoint
            method: "POST",
            body: formData.current, // This is your file object
        })
            .then(
                (response) => response.json() // if the response is a JSON object
            )
            .then(
                (success) => {
                    success.student_current_major = currentStudentMajor;
                    success.student_future_major = futureStudentMajor;
                    setStudentData(success);
                    console.log("The data of the student", success);
                    getRecognizedSubjects(
                        success,
                        currentStudentMajorId + "-" + futureStudentMajorId
                    );
                    deletePdfFile();
                    setIsLoading(false);
                } // Handle the success response object
            )
            .catch(
                (error) => console.log(error) // Handle the error response object
            );
    };

    const deletePdfFile = () => {
        fetch("http://127.0.0.1:8000/api/delete-pdf-file", {
            method: "GET",
        })
            .then(
                (response) => response.json() // if the response is a JSON object
            )
            .then(
                (success) => {
                    console.log(success);
                    setIsLoading(false);
                } // Handle the success response object
            )
            .catch(
                (error) => console.log(error) // Handle the error response object
            );
    };

    const getSubjects = async (major) => {
        let subjects;

        await fetch("http://127.0.0.1:8000/api/get-major-data", {
            method: "POST",
            body: major,
        })
            .then(
                (response) => response.json() // if the response is a JSON object
            )
            .then(
                (success) => {
                    subjects = success;
                    console.log(success);
                    setIsLoading(false);
                } // Handle the success response object
            )
            .catch(
                (error) => console.log(error) // Handle the error response object
            );

        return subjects;
    };

    const getRecognizedSubjects = async (student, transfer) => {
        let requiredSubjects = [];
        let temp;
        let recognizedSubjects = [];
        let transferData = [];
        console.log(currentStudentMajor);
        for (const x in currentStudentMajor) {
            for (const y in currentStudentMajor[x]) {
                for (const z in student.student_grades) {
                    if (
                        currentStudentMajor[x][y].name ==
                        student.student_grades[z].name
                    ) {
                        console.log("Match: ", currentStudentMajor[x][y].name);
                        temp = currentStudentMajor[x][y];
                        temp.grade = student.student_grades[z].grade;
                        requiredSubjects.push(temp);
                    }
                }
            }
        }

        console.log(requiredSubjects);

        await fetch("http://127.0.0.1:8000/api/get-transfer-data", {
            method: "POST",
            body: transfer,
        })
            .then(
                (response) => response.json() // if the response is a JSON object
            )
            .then(
                (success) => {
                    transferData = success;
                    console.log(success);
                    setIsLoading(false);
                } // Handle the success response object
            )
            .catch(
                (error) => console.log(error) // Handle the error response object
            );

        console.log(transferData);

        for (const i in transferData) {
            for (const j in transferData[i].requiredSubjects) {
                for (const k in requiredSubjects) {
                    console.log(
                        transferData[i].requiredSubjects[j],
                        requiredSubjects[k].id
                    );
                    if (
                        transferData[i].requiredSubjects[j] ==
                        requiredSubjects[k].id
                    ) {
                        console.log(
                            "Recognized subject: ",
                            transferData[i].recognizedSubject
                        );

                        for (const l in futureStudentMajor) {
                            for (const m in futureStudentMajor[l]) {
                                if (
                                    transferData[i].recognizedSubject ==
                                    futureStudentMajor[l][m].id
                                ) {
                                    temp = futureStudentMajor[l][m];
                                    temp.grade = requiredSubjects[k].grade;
                                    recognizedSubjects.push(
                                        futureStudentMajor[l][m]
                                    );
                                }
                            }
                        }

                        break;
                    }
                }
            }
        }

        console.log(
            "Required: ",
            requiredSubjects,
            "Recognized",
            recognizedSubjects
        );

        setRequiredStudentSubjects(requiredSubjects);
        setRecognizedStudentSubjects(recognizedSubjects);
    };

    return (
        <div className="HomePage">
            <div className="home-page-content">
                <h1>Prebacivanje smjerova</h1>

                <div className="select-majors">
                    <label htmlFor="current-major">
                        Studentov trenutni smjer:
                    </label>

                    <select
                        name="current-major"
                        id="current-major-select"
                        onChange={() => handleCurrentMajorSelect(event)}
                    >
                        <option value=""></option>
                        {majorsData &&
                            majorsData.map((currentMajor) => (
                                <option
                                    key={currentMajor.id}
                                    value={currentMajor.id}
                                >
                                    {currentMajor.name}
                                </option>
                            ))}
                    </select>

                    <label htmlFor="future-major">
                        Smjer na koji se student prebacuje:
                    </label>

                    <select
                        name="future-major"
                        id="future-major-select"
                        onChange={() => handleFutureMajorSelect(event)}
                    >
                        <option value=""></option>
                        {majorsData &&
                            majorsData.map((futureMajor) => (
                                <option
                                    key={futureMajor.id}
                                    value={futureMajor.id}
                                >
                                    {futureMajor.name}
                                </option>
                            ))}
                    </select>
                </div>

                <div className="file-upload-div">
                    <p></p>
                    <label htmlFor="file-upload" className="custom-file-upload">
                        Browse
                    </label>
                    <input
                        type="file"
                        id="file-upload"
                        onChange={() => handleFileUpload(event)}
                    />
                    <p>{fileName}</p>
                    <button onClick={handleFileUploadClick}>Confirm</button>
                </div>

                {isLoading && <p>Loading...</p>}
                {studentData && (
                    <div className="student-info">
                        <p>Student: {studentData.student_name}</p>

                        <h2>Promjena studija: </h2>
                        <p>{transferId}</p>

                        <h2>Ocjene:</h2>
                        <div className="student-grades">
                            {studentData.student_grades.map((subject) => (
                                <p key={subject.name}>
                                    {subject.name} {subject.grade}
                                </p>
                            ))}
                        </div>

                        <h2>Prepoznate ocjene:</h2>
                        <div className="required-student-grades">
                            {requiredStudentSubjects &&
                                requiredStudentSubjects.map((subject) => (
                                    <p key={subject.name}>
                                        {subject.name} {subject.grade}
                                    </p>
                                ))}
                        </div>

                        <h2>Priznate ocjene:</h2>
                        <div className="recognized-student-grades">
                            {recognizedStudentSubjects &&
                                recognizedStudentSubjects.map((subject) => (
                                    <p key={subject.name}>
                                        {subject.name} {subject.grade}
                                    </p>
                                ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default HomePage;
