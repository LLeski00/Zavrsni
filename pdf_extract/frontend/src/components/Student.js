import React, {Component} from "react";

const Student = () => {

    const getStudentDetails = () => {
        fetch('/api/get-student' + '?code=' + 'QZQKUS')
        .then((response) => response.json())
        .then((data) => {
            console.log(data.votes_to_skip);
        });
    };

    return (
        <div className="Student">
            <div className="student-content">
                <button onClick={getStudentDetails}>Click</button>
            </div>
        </div>
    );
}
 
export default Student;