url = 'https://cbkm-analytics-services.herokuapp.com'

key = 'grabittest1565729801986'
var  socket = io('https://cbkm-analytics-services.herokuapp.com/analytics');
function  send(act) {
data={
appID:key,
action:act,
//myname:"myname"
}
socket.emit('save', data);
// window.location.href = link
}
function  sendN(act, name) {
    // alert(act+name)
    data={
    appID:key,
    action:act,
    name:name
    }
    socket.emit('save', data);
    // window.location.href = link
    }
function  sendNI(act, name, id) {
    // alert(act+name+id)
    data={
    appID:key,
    action:act,
    name:name,
    id:id
    }
    socket.emit('save', data);
    // window.location.href = link
    }

function getViews(id){
    axios.defaults.headers.common['appID'] = key
    axios.post(`${url}/analytics/specific`,{
        id:id
    })
    .then(res=>{
        console.log(res.data.data.length)
        document.getElementById(`view${id}`).innerHTML = res.data.data.length;
    })
}
