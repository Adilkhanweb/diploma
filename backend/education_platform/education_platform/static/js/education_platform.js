var phoneMask = IMask(
    document.getElementById('phone-mask'), {
        mask: '+{7}(000)000-00-00',
        lazy: false,  // make placeholder always visible
        // placeholderChar: ''     // defaults to '_'
    });
