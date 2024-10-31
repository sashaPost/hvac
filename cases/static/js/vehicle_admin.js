document.addEventListener('DOMContentLoaded', function() {
    // Function to handle engine capacity visibility
    function handleEngineCapacity() {
        // Try both possible select IDs (standalone and inline forms)
        const vehicleTypeSelect = document.querySelector('#id_vehicle_type') ||
                                document.querySelector('#id_vehicle-0-vehicle_type');

        if (!vehicleTypeSelect) {
            console.log('Vehicle type select not found');
            return;
        }

        // Find the engine capacity field container
        const engineCapacityContainer = document.querySelector('.field-engine_capacity') ||
                                      document.querySelector('.form-row.field-engine_capacity');

        if (!engineCapacityContainer) {
            console.log('Engine capacity container not found');
            return;
        }

        function toggleEngineCapacity() {
            // Get the selected option's text
            const selectedOption = vehicleTypeSelect.options[vehicleTypeSelect.selectedIndex];
            const isElectric = selectedOption.text.includes('Electric');

            console.log('Selected vehicle type:', selectedOption.text);
            console.log('Is electric:', isElectric);

            // Show/hide the engine capacity field
            engineCapacityContainer.style.display = isElectric ? 'none' : 'block';

            // Clear value if electric
            if (isElectric) {
                const engineCapacityInput = document.querySelector('#id_engine_capacity') ||
                                          document.querySelector('#id_vehicle-0-engine_capacity');
                if (engineCapacityInput) {
                    engineCapacityInput.value = '';
                }
            }
        }

        // Initial state
        toggleEngineCapacity();

        // Add change event listener
        vehicleTypeSelect.addEventListener('change', toggleEngineCapacity);
    }

    // Initialize for both inline and standalone forms
    handleEngineCapacity();
});