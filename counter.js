import React,{useState} from 'react'

export default function Counter()
{
    const[counter,setCounter]=useState(0)
    const[name,setName]=useState("")
  return (
    <>
    <p>the counter is:{counter}</p>
    <button onClick={(e)=>setCounter(counter+1)}>click to add 1</button>
    <button onClick={(e)=>setCounter(0)}>click to 0</button>
    </>
  )
}
