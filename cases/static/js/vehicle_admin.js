document.addEventListener('DOMContentLoaded', function() {
    let vehicleTypeSelect;

    function toggleFuelEngineInline() {
        vehicleTypeSelect = document.getElementById('id_vehicle_type'); // Assign value inside this function
        console.log('vehicleTypeSelect:', vehicleTypeSelect);

        const engineCapacity = document.querySelector('.field-engine_capacity'); // Or use '#engine-capacity-id'
        console.log('engineCapacity:', engineCapacity);

        console.log('vehicleTypeSelect.value', vehicleTypeSelect.value)
        if (vehicleTypeSelect.value === '1' || vehicleTypeSelect.value === '3') {
            console.log('if STATEMENT WAS TRIGGERED')
            engineCapacity.style.display = 'block'; // Or another appropriate display value
        } else {
            engineCapacity.style.display = 'none';
        }
    }

    toggleFuelEngineInline(); // Initial call to populate the variable
    vehicleTypeSelect.addEventListener('change', toggleFuelEngineInline);
});

// $(document).ready(function() {
//     function toggleFuelEngineInline() {
//         var vehicleTypeSelect = $('#id_vehicle_type');
//         console.log('vehicleTypeSelect:', vehicleTypeSelect);
//
//         var engineCapacity = $('#id_engine_capacity');
//         console.log('engineCapacity:', engineCapacity);
//
//         console.log('vehicleTypeSelect.val():', vehicleTypeSelect.val());
//         if (vehicleTypeSelect.val() === '1' || vehicleTypeSelect.val() === '3') {
//             console.log('is STATEMENT WAS TRIGGERED');
//             engineCapacity.show();
//         } else {
//             engineCapacity.hide();
//         }
//     }
//
//     toggleFuelEngineInline();
//     $('#id_engine_capacity').change(toggleFuelEngineInline);
// });