// NAVBAR
function activeShadowNavBar(){
    const navbar = document.getElementById('navbar');
    if(scrollY > 50) navbar.classList.add('active-header'); else navbar.classList.remove('active-header')
}

// MENU MOBILE
const showMenu = (navId, toggleId) =>{
    const nav = document.getElementById(navId)
    const toggle = document.getElementById(toggleId)
    if(nav && toggle){
        nav.addEventListener('click',()=>{
            nav.classList.toggle('active-bx');
            toggle.classList.toggle('active-menu-mobile');

        })
    }    
}
showMenu('bx', 'menu-mobile')


// REMOVE ALERT
const alertXMark = document.getElementById('alert-xmark');
if(alertXMark){
    alertXMark.addEventListener('click', (event)=>{
        event.preventDefault();
        const alert = document.getElementById('alert');
        // alert.classList.remove('alert');

        alert.style.animation = '';

        setTimeout(function(){
            // alert.classList.add('alert-hide');
            alert.style.animation = 'alert-right-hide .7s ease forwards';
        },10);
        
    })
}


// EDITAR POST
function elementEditarPost(){
    const link_editar_post = document.getElementById('link-editar-post');
    if(link_editar_post){
        link_editar_post.addEventListener('click',(event)=>{
            event.preventDefault();
            
            // HIDE EDITAR/EXCLUIR POST
            const elementEditarExcluirPost = document.getElementById('links-editar-and-excluir-post');
            elementEditarExcluirPost.classList.add('hide')

            // SHOW EDITAR PERFIL
            const elementEditarPerfil = document.getElementById('form-editar-post')
            elementEditarPerfil.classList.remove('hide')
            
        })
    }

}
// CANCELAR EDIÇÃO DE POST
function elementCancelarEdicaoPost(){
    const link_cancelar_post = document.getElementById('link-cancelar-edicao')
    if(link_cancelar_post){
        link_cancelar_post.addEventListener('click', (event)=>{
            event.preventDefault();

            // SHOW EDITAR/EXCLUIR POST
            const elementEditarExcluirPost = document.getElementById('links-editar-and-excluir-post');
            elementEditarExcluirPost.classList.remove('hide')

            // HIDE EDITAR PERFIL
            const elementEditarPerfil = document.getElementById('form-editar-post')
            elementEditarPerfil.classList.add('hide')
        })
    }
}
// POPUP EXCLUIR POST
function elementExcluirPost(){
    const link_excluir_post = document.getElementById('link-excluir-post')
    if(link_excluir_post){
        link_excluir_post.addEventListener('click', (event)=>{
            event.preventDefault();

            const popup_wraper = document.getElementById('popup-wraper')
            popup_wraper.classList.remove('hide')
            popup_wraper.classList.add('popup-wraper')
        }) 
    }
}

window.onload = () =>{
    elementEditarPost();
    elementCancelarEdicaoPost();
    elementExcluirPost();
}






