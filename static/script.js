document.getElementById("searchForm").addEventListener('submit', async function (event) {
    event.preventDefault();
    const phoneNumber = document.getElementById("phoneNumber").value;

    if (!phoneNumber) {
        alert("Please enter a valid phone number");
        return;
    }

    if(phoneNumber.length>10){
        alert("Phone number cannot be more than 10 digits")
        return;
    }

    // Disable the upload form while search results are being fetched
    document.getElementById('uploadForm').querySelector('button').disabled = true;

    document.getElementById('loading').style.display = 'block';

    try {
        const response = await fetch('http://192.168.10.130:5000/getdata',{method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({phoneNo:phoneNumber})

        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        // If data is found, populate the form fields
        if (data) {
            document.getElementById('results').style.display='block';

            document.getElementById('email').value = data['email'] || "Not Found";
            document.getElementById('jobTitle').value = data['jobTitle'] || "Not Found";
            document.getElementById('currentOrganization').value = data['organization'] || "Not Found";
            document.getElementById('frontend_skills').value=data['fs']||'Not found';
            document.getElementById('backend_skills').value=data['bs']||'Not found';
            document.getElementById('other_skills').value=data['os']||'Not found';
            document.getElementById('programming_languages').value=data['pl']||'Not found';
            document.getElementById('databases').value=data['ds']||'Not found';
         
            document.getElementById('name').value = data['name'] || "Not Found";
            document.getElementById('degree1').value=data['degree1']||'Not Found'
            document.getElementById('college').value=data['college1']||'Not Found'
            document.getElementById('percentage1').value=data['percentage1']||'Not found'
            document.getElementById('passOutYear1').value=data['passOutYear1']||'Not Found'
            document.getElementById('yearsOfExp').value=data['yearsOfExp']||'Not Found'
            document.getElementById('phoneNo').value = phoneNumber;
            document.getElementById('summary').value=data['summary']||'Not found'
            document.getElementById('college2').value=data['college2']||'Not found'
            document.getElementById('degree2').value=data['degree2']||'Not found'
            document.getElementById('passOutYear2').value=data['passOutYear2']||'Not found'
            document.getElementById('percentage2').value=data['percentage2']||'Not found'
            document.getElementById('countryCode').value=data['countryCode']||'Not found'

            document.getElementById("skillsSection").style.display = 'block';

            document.getElementById('profileSummarySection').style.display = 'block';
            document.getElementById("educationSection").style.display = 'block';
            document.querySelector('.right-side').style.display = 'block';
        } else {
            alert("No data found for the given phone number.");
        }

    } catch (error) {
        console.error("Error fetching data:", error);
        alert("An error occurred while fetching data. Please try again.");
    } finally {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('uploadForm').querySelector('button').disabled = false; // Re-enable the upload form
    }
});


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
function resetFormFields(){
    const fields = ['email', 'jobTitle', 
        'currentOrganization', 'programming_languages', 'frontend_skills', 
        'backend_skills', 'databases', 'other_skills', 'name', 'college', 'degree1','percentage1',
         'passOutYear1', 'yearsOfExp', 'phoneNo','summary','college2','degree2','passOutYear2','percentage2','countryCode'];
    fields.forEach(field=>{
        document.getElementById(field).value=""
    })
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
    document.getElementById('searchForm').querySelector('button').disabled=true
    resetFormFields()
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
        console.log(result2)

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
        document.getElementById('degree1').value=result2['degree'] || "Not found"
        document.getElementById('percentage1').value=result2['percentage1']||'Not found'
        document.getElementById('passOutYear1').value=result2['passOutYear1'] ||"Not found"
        document.getElementById('phoneNo').value=result2['phoneNo'] ||"Not found"
        document.getElementById('yearsOfExp').value=result2['yearsOfExp']||"Not found"
        document.getElementById('summary').value=result2['summary']||'Not found'
        document.getElementById('college2').value=result2['deg2list']['college2']||'Not found'
        document.getElementById('degree2').value=result2['deg2list']['degree2']||'Not found'
        document.getElementById('passOutYear2').value=result2['deg2list']['passOutYear2']||'Not found'
        document.getElementById('percentage2').value=result2['deg2list']['percentage2']||'Not found'
        document.getElementById("countryCode").value=result2['countryCode']||'Not found'


        document.getElementById("skillsSection").style.display='block'
        document.getElementById('profileSummarySection').style.display='block'
        document.getElementById("educationSection").style.display='block'
        document.querySelector('.right-side').style.display = 'block'

    }catch(error){
        console.error("Error parsing resume:", error)
        alert("An error occurred  while parsing the resume. Please try again")
    }finally{
        document.getElementById('loading').style.display='none'
        document.getElementById('searchForm').querySelector('button').disabled=false
    }   

})



document.getElementById("editForm").addEventListener('submit',async function (event) {
    event.preventDefault()
    const formData=new FormData(event.target)
    const data={
        email:document.getElementById('email').value,
        jobTitle:document.getElementById('jobTitle').value,
        organization:document.getElementById('currentOrganization').value,
        pl:document.getElementById('programming_languages').value,
        fs:document.getElementById('frontend_skills').value,
        bs:document.getElementById('backend_skills').value,
        ds:document.getElementById('databases').value,
        os:document.getElementById('other_skills').value,
        name:document.getElementById('name').value,
        college1:document.getElementById("college").value,
        degree1:document.getElementById("degree1").value,
        percentage1:document.getElementById('percentage1').value,
        passOutYear1:document.getElementById('passOutYear1').value,
        phoneNo:document.getElementById('phoneNo').value,
        yearsOfExp:document.getElementById('yearsOfExp').value,
        summary:document.getElementById('summary').value,
        college2:document.getElementById('college2').value,
        degree2:document.getElementById('degree2').value,
        passOutYear2:document.getElementById('passOutYear2').value,
        percentage2:document.getElementById('percentage2').value,
        countryCode:document.getElementById('countryCode').value
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

