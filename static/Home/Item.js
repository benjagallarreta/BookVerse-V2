<script>
document.addEventListener('DOMContentLoaded', function() {
    const estrellas = document.querySelectorAll('.estrellas label');

    estrellas.forEach(star => {
        star.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            const radios = document.querySelectorAll('.star-radio');
            
            radios.forEach(radio => {
                if (radio.value <= value) {
                    radio.checked = true;
                } else {
                    radio.checked = false;
                }
            });
        });
    });
});
</script>
