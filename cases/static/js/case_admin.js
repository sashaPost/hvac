document.addEventListener('DOMContentLoaded', function() {
    let vehicleTypeSelect;

    function toggleFuelEngineInline() {
        vehicleTypeSelect = document.getElementById('id_vehicle-0-vehicle_type'); // Assign value inside this function
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
