import React, { Component, useEffect, useRef } from "react";
import { useState } from "react";

const RecognizedSubjects = ({
    student,
    transfer,
    requiredStudentSubjects,
    setRequiredStudentSubjects,
    recognizedStudentSubjects,
    setRecognizedStudentSubjects,
    currentStudentMajor,
    futureStudentMajor,
    setIsLoading,
}) => {
    useEffect(() => {
        getRequiredSubjects(student, transfer);
    }, [student]);

    const [transferData, setTransferData] = useState(null);

    const getRequiredSubjects = async (student, transfer) => {
        let requiredSubjects = [];
        let temp;
        let transferData = [];

        await fetch("http://127.0.0.1:8000/api/get-transfer-data", {
            method: "POST",
            body: transfer,
        })
            .then((response) => response.json())
            .then((success) => {
                transferData = success;
                setTransferData(success);
                setIsLoading(false);
            })
            .catch((error) => console.log(error));

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

        console.log(
            "Subjects that match the current major: ",
            requiredSubjects
        );

        setRequiredStudentSubjects(requiredSubjects);
        getRecognizedSubjects(requiredSubjects, transferData);
    };

    const getRecognizedSubjects = (requiredSubjects, transferData) => {
        let tempGrades = [];
        let matches;
        let recognizedSubjects = [];
        let temp;

        for (const i in transferData) {
            matches = 0;
            for (const j in transferData[i].requiredSubjects) {
                for (const k in requiredSubjects) {
                    if (
                        transferData[i].requiredSubjects[j] ==
                        requiredSubjects[k].id
                    ) {
                        matches++;
                        console.log(
                            "Match: ",
                            requiredSubjects[k].name,
                            " ID: ",
                            requiredSubjects[k].id,
                            "Grade: ",
                            requiredSubjects[k].grade
                        );
                        tempGrades.push(requiredSubjects[k].grade);

                        if (
                            matches == transferData[i].requiredSubjects.length
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
                                        temp.grade = 0;

                                        for (const ind in tempGrades) {
                                            console.log(
                                                temp.grade,
                                                "=",
                                                temp.grade,
                                                "+",
                                                tempGrades[ind]
                                            );
                                            temp.grade =
                                                Number(temp.grade) +
                                                Number(tempGrades[ind]);
                                        }
                                        temp.grade = Math.round(
                                            temp.grade / tempGrades.length
                                        );

                                        recognizedSubjects.push(temp);
                                        tempGrades.length = 0;
                                        break;
                                    }
                                }
                            }
                        }
                    }
                }
            }
            tempGrades.length = 0;
        }

        console.log("Recognized", recognizedSubjects);

        setRecognizedStudentSubjects(recognizedSubjects);
    };

    const handleSubjectUpdate = (event) => {
        let requiredSubjects = requiredStudentSubjects;
        console.log(event.target.getAttribute("custom-key"));
        console.log(event.target.value);
        let subjectId = event.target.getAttribute("custom-key");
        let subjectGrade = event.target.value;
        for (const i in requiredSubjects) {
            if (requiredSubjects[i].id == subjectId) {
                console.log(
                    "Changed subject: ",
                    requiredSubjects[i].name,
                    " Grade: ",
                    requiredSubjects[i].grade
                );
                if (subjectGrade < 2 || subjectGrade > 5) {
                    requiredSubjects.splice(i, 1);
                    setRequiredStudentSubjects(requiredSubjects);
                    getRecognizedSubjects(requiredSubjects, transferData);
                    return;
                } else {
                    requiredSubjects[i].grade = subjectGrade;
                    setRequiredStudentSubjects(requiredSubjects);
                    getRecognizedSubjects(requiredSubjects, transferData);
                    return;
                }
            }
        }

        if (subjectGrade < 2 || subjectGrade > 5) return;

        for (const x in currentStudentMajor) {
            for (const y in currentStudentMajor[x]) {
                if (currentStudentMajor[x][y].id == subjectId) {
                    console.log(
                        "Changed subject: ",
                        currentStudentMajor[x][y].name
                    );
                    let temp = currentStudentMajor[x][y];
                    temp.grade = subjectGrade;
                    requiredSubjects.push(temp);
                    setRequiredStudentSubjects(requiredSubjects);
                    getRecognizedSubjects(requiredSubjects, transferData);
                    return;
                }
            }
        }
    };

    return (
        <div className="RecognizedSubjects">
            <div className="recognized-subjects-content">
                <div className="transfer-block">
                    <div className="current-student-major">
                        <h2>Smjer sa kojeg se student prebacuje: </h2>
                        {requiredStudentSubjects &&
                            Object.keys(currentStudentMajor).map(
                                (keyName, i) => (
                                    <React.Fragment key={i}>
                                        <div className="current-student-major-semester">
                                            <form className="grades-form">
                                                <h3>{keyName}. semestar</h3>
                                                {currentStudentMajor[
                                                    keyName
                                                ].map((subject, index) => (
                                                    <div
                                                        className="passed-subject"
                                                        key={index}
                                                    >
                                                        <p>{subject.name}</p>
                                                        <input
                                                            type="text"
                                                            custom-key={
                                                                subject.id
                                                            }
                                                            defaultValue={
                                                                requiredStudentSubjects[
                                                                    requiredStudentSubjects.findIndex(
                                                                        (x) =>
                                                                            x.id ==
                                                                            subject.id
                                                                    )
                                                                ] &&
                                                                requiredStudentSubjects[
                                                                    requiredStudentSubjects.findIndex(
                                                                        (x) =>
                                                                            x.id ==
                                                                            subject.id
                                                                    )
                                                                ].grade
                                                            }
                                                            onChange={() =>
                                                                handleSubjectUpdate(
                                                                    event
                                                                )
                                                            }
                                                        ></input>
                                                    </div>
                                                ))}
                                            </form>
                                        </div>
                                    </React.Fragment>
                                )
                            )}
                    </div>

                    <div className="recognized-student-grades">
                        <h2>Priznate ocjene:</h2>
                        <div className="recognized-student-grades-list">
                            {recognizedStudentSubjects &&
                                recognizedStudentSubjects.map((subject) => (
                                    <p key={subject.name}>
                                        {subject.name} | Ocjena: {subject.grade}
                                    </p>
                                ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RecognizedSubjects;
