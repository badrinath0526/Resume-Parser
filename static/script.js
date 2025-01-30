function toggleSection(event){
    const sectionContent=event.target.nextElementSibling;
    const toggleSymbol=event.target.querySelector('.toggle-symbol')
    const currentText=toggleSymbol.innerHTML

    if(sectionContent.style.display==='block'){
        sectionContent.style.display='none'
        toggleSymbol.innerHTML='(+)'
    }else{
        sectionContent.style.display='block'
        toggleSymbol.innerHTML='(-)'
    }
}

document.querySelectorAll('.section h4').forEach(sectionHeader => {
    sectionHeader.addEventListener('click', toggleSection);
});

function toggleInput(event) {
    const span = event.target;
    const input = span.nextElementSibling;

    // Hide span (read-only text) and show input field for editing
    span.style.display = 'none';
    input.style.display = 'block';

    input.focus();  // Focus on input field for editing
}

// Add event listeners to all editable spans to make them clickable
document.querySelectorAll('.result-row span').forEach(span => {
    span.addEventListener('click', toggleInput);
});

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
    document.querySelector('.right-side').style.display = 'none'

    try{
        const [response1,response2]= await Promise.all
        ([fetch('/parse-resume',{method:'POST',body:formData}),
        fetch("http://192.168.10.130:5000/extract",{method:'POST',body:formData})
    ]);

        if(!response1.ok){
            throw new Error(`HTTP error! status: ${response1.status}`)
        }
        if(!response2.ok){
            throw new Error(`HTTP error! status: ${response2.status}`)
        }
        const result1= await response1.json()
        const result2=await response2.json()
        console.log(result1)
        // console.log(result2)

        document.getElementById('results').style.display='block';
        document.getElementById('email').value=result1['Email'] || "Not Found"
        document.getElementById('jobTitle').value=result1['Job title'] || "Not found";
        document.getElementById('currentOrganization').value=result1['Current organization']|| "Not found"
        document.getElementById('programming_languages').value=result1['programming_languages'] || "Not found"
        document.getElementById('frontend_skills').value=result1['frontend_skills']||"Not found"
        document.getElementById('backend_skills').value=result1['backend_skills']||"Not found"
        document.getElementById('databases').value=result1['databases']||'Not found'
        document.getElementById('other_skills').value=result1['other_skills']||'Not found'
        document.getElementById('name').value=result2['name'] || "Not found"
        document.getElementById("college").value=result2['college']||"Not found"
        document.getElementById('degree1').value=result2['degree1'] || "Not found"
        document.getElementById('degree2').value=result2['degree2'] || "Not found"
        document.getElementById('passOutYear').value=result2['passOutYear'] ||"Not found"
        document.getElementById('phoneNo').value=result2['phoneNo'] ||"Not found"
        document.getElementById('yearsOfExp').value=result2['yearsOfExp']||"Not found"
        document.getElementById('summary').value=result2['summary']||'Not found'
        document.getElementById('college2').value=result2['degree2']['college2']||'Not found'
        document.getElementById('degree2').value=result2['degree2']['degre2']||'Not found'
        document.getElementById('passOutYear2').value=result2['degree2']['passOutYear']||'Not found'
        document.getElementById('percentage').value=result2['degree2']['percentage']||'Not found'


        document.getElementById("skillsSection").style.display='block'
        document.getElementById('profileSummarySection').style.display='block'
        document.getElementById("educationSection").style.display='block'
        document.querySelector('.right-side').style.display = 'block'

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
        const res1=await fetch("/add-job-title",{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({jobTitle:data.jobTitle})
        })
        const job_title_result=await res1.json()
        if(res1.ok){
            console.log(job_title_result.message)
        }else{
            console.error(job_title_result.error)
        }
    }catch(error){
        console.error("Error communicating with local Flask API",error)
        alert("an error occurred storing job title")
    }
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

