document.addEventListener("DOMContentLoaded", function (event) {
    console.log("hola");
    const imagesContainer = document.getElementById('main');
    const csrfToken = document.querySelector("[name='csrfmiddlewaretoken']").getAttribute("value")
    imagesContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('delete-link')) {
            event.preventDefault();

            if (confirm("Seguro de que deseas eliminar este elemento?")) {
                var deleteUrl = event.target.getAttribute('href');

                fetch(deleteUrl, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                })
                    .then(response => {
                        if (response.status === 200) {
                            event.target.closest(".deletable-list-item").remove()
                            alert("El elemento se ha eliminado correctamente ")
                            return;
                        }
                        alert('Error al eliminar el elemento.');
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }
        }
    });

});


