send_msg = async ()=>{

 let msg_survey_no = document.getElementById('msg_survey_no') || 0
 let msg_content = document.getElementById('msg_content')

 let source = '/msg'
 let payload = { 
     method: "POST",
     headers: {
               'Content-Type': 'application/json'
               },
     body: JSON.stringify({
                 "c_fullname": `${c_fullname}`,
                 "c_phone": `${c_phone}`,
                 "survey_no": `${msg_survey_no.value}`, 
                 "message": `${msg_content.value}` 
             }) 
     }

 const response = await fetch(source,payload);
 const data = await response.json()
       if (data['status']=='ok'){
         alert('Message sent to RBK.')
         msg_content.value = ''
       }
}