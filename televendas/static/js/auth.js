logado = sessionStorage.getItem("nome");
email_logado = sessionStorage.getItem("email");

if (!logado){
    alert("Faça o login para visualizar");
    window.location.href = "https://portal.a5solutions.com:8092/login";
}

if (email_logado !== 'admin@televendas.com'){
    alert("Você não tem permissão para acessar esse conteúdo");
    window.location.href = "https://portal.a5solutions.com:8092/";
}