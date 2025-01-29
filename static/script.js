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
        console.log(result)

        const response2=await fetch("http://192.168.10.130:5000/extract",{
            method:'POST',
            body:formData
        })
        if(!response2.ok){
            throw new Error(`HTTP error! status: ${response2.status}`)
        }

        const result2=await response2.json()
        console.log(result2)

        document.getElementById('results').style.display='block';
        document.getElementById('email').value=result['Email'] || "Not Found"
        document.getElementById('jobTitle').value=result['Job title'] || "Not found";
        document.getElementById('currentOrganization').value=result['Current organization']|| "Not found"
        document.getElementById('name').value=result2['name'] || "Not found"
        document.getElementById("college").value=result2['college']||"Not found"
        document.getElementById('degree').value=result2['degree'] || "Not found"
        document.getElementById('passOutYear').value=result2['passOutYear'] ||"Not found"
        document.getElementById('phoneNo').value=result2['phoneNo'] ||"Not found"
        document.getElementById('yearsOfExp').value=result2['yearsOfExp']||"Not found"

        

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
        name:document.getElementById('name').value,
        college:document.getElementById("college").value,
        degree:document.getElementById("degree").value,
        passOutYear:document.getElementById('passOutYear').value,
        phoneNo:document.getElementById('phoneNo').value,
        yearsOfExp:document.getElementById('yearsOfExp').value
    };

    try{
        const response=await fetch('http://192.168.10.130:5000/values',{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify(data)
        })
        if(!response.ok){
            throw new Error(`HTTP error! status: ${response.status}`)
        }
        const res=await response.json()
        console.log(res)
        alert(res.message)
    }catch(error){
        console.error("Error submitting resume: ",error)
        alert("An error occurred while submitting the details. Please try again")
    }
})