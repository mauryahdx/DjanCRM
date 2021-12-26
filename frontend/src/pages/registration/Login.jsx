
import { useEffect, useState} from "react";
const Login = () => {


    const [html, setHtml] = useState([]);

    useEffect(() => {
        fetch('login')
        .then(response => response.text())
        .then(text => {
            setHtml(text)
            //var parser = new DOMParser();
            //setHtml(parser.parseFromString(text, "text/html"));
         
        })
    }, [])



//var markup
//var x =0;
//fetch('login')
//    .then(res => markup=res.text())
//    .then(res => {
//        //console.log(res)
//        //return res
//        x=x+1;
//        console.log(x)
//       var parser = new DOMParser();
//       markup = parser.parseFromString(res, "text/html");
//        console.log(markup)
//        })
//    .catch(err => console.error(err));
//console.log("YO",markup)
    //"<p>foo bar</p>"<div dangerouslySetInnerHTML={{__html: html}} />
    return (
     
        <><div dangerouslySetInnerHTML={{__html: html}} /></>
    
    )
}

export default Login
