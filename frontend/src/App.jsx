import {useState} from 'react';
function questionInput(){
  const [content, setContent]=useState('');
  const [difficulty, setDifficulty]=useState('');
  const [numberOfQuestions, setNumberOfQuestions]=useState('');
  const [questions, setQuestions]=useState([]);
  async function backendCall(){
  const response=await fetch('http://127.0.0.1:8000/generate_questions_endpoint', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      content: content,
      difficulty: difficulty,
      num_questions: numberOfQuestions
    })
  });
  const data=await response.json();
  setQuestions(data);
  } 
  return (
    <>
      <textarea value={content} onChange={(e) => setContent(e.target.value)} />
      <input value={difficulty} onChange={(e) => setDifficulty(e.target.value)} />
      <input value={numberOfQuestions} onChange={(e) => setNumberOfQuestions(e.target.value)} />
      <button onClick={backendCall}>Generate Questions</button>
      <ul>
        {questions.map((q,index)=>(
          <li key={index}>
            Question : {q.question}<br />
            Answer : {q.answer}
          </li>
        ))
        }
      </ul>
    </>
  )
}

export default questionInput;

