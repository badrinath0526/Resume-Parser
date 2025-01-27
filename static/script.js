document.getElementById("uploadForm").addEventListener('submit',async function (event) {
    event.preventDefault()
    const fileInput=document.getElementById('file')
    const file=fileInput.files[0]
    if(!file){
        alert("Please select a file to upload")
        return;
    }
    const formData=new FormData()
    formData.append('file',file)

    document.getElementById('loading').style.display='block'
    document.getElementById('results').style.display='none'

    try{
        const response= await fetch('/parse-resume',{
            method:'POST',
            body:formData
        });
        if(!response.ok){
            throw new Error(`HTTP error! status: ${response.status}`)
        }

        const result= await response.json()
        

        document.getElementById('results').style.display='block';
        document.getElementById('email').value=result['Email'] || "Not Found"
        document.getElementById('jobTitle').value=result['Job title'] || "Not found";
        document.getElementById('currentOrganization').value=result['Current organization']|| "Not found"

    }catch(error){
        console.error("Error parsing resume:", error)
        alert("An error occurred  while parsing the resume. Please try again")
    }finally{
        document.getElementById('loading').style.display='none'
    }

})
document.getElementById("editForm").addEventListener('submit',async function (event) {
    event.preventDefault()
    // const formData=new FormData(event.target)
    const data={
        email:document.getElementById('email').value,
        jobTitle:document.getElementById('jobTitle').value,
        currentOrganization:document.getElementById('currentOrganization').value,
    };

    try{
        const response=await fetch('/submit-resume',{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify(data)
        })
        if(!response.ok){
            throw new Error(`HTTP error! status: ${response.status}`)
        }
        const result=await response.json()
        alert(result.message || "Details successfully submitted!")
    }catch(error){
        console.error("Error submitting resume: ",error)
        alert("An error occurred while submitting the details. Please try again")
    }
})