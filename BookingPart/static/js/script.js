document.addEventListener('DOMContentLoaded', function() {
    const busLayout = document.getElementById('bus-layout');
    const busLayout2 = document.getElementById('bus-layout2');
    const bookButton = document.getElementById('book-button');
    const cancelButton = document.getElementById('cancel-button');
    const bdisplay = document.getElementById('bDisplay');
    const selectedSeats = new Set();
    const timeSlotSelect = document.getElementById('time_slot');
    var allow = true

    const urlParams = new URLSearchParams(window.location.search);
    // const userEmail = session['username'];
    // console.log(userEmail);
    const userEmail = logged_in_user_email;
    console.log("uuu");
    console.log(userEmail);

    // timeSlotSelect.addEventListener('change', function() {
    //     // Get the selected option
    //     const selectedOption = timeSlotSelect.options[timeSlotSelect.selectedIndex];
        
    //     // Update the hidden input fields with the selected values for route ID and capacity
    //     document.getElementById('time_slot').value = selectedOption.dataset;
    // });
    

    const capacity = urlParams.get('route_id')[0];
        // Fetch booked seats function
    function fetchBookedSeats() {
        // const urlParams = new URLSearchParams(window.location.search);
        // const licencePlateNumber = urlParams.get('licence_plate_number');

        const urlParams = new URLSearchParams(window.location.search);
        const _date = urlParams.get('date');
        const route = urlParams.get('route_id');

        // const userEmail = 'exampsfle_email@example.com'; 

        // const userEmail = session['emailID'];
        const userEmail = logged_in_user_email;


        // console.log(licencePlateNumber)
        fetch('/fetch-booked-seats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ _date: _date, route: route})
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to fetch booked seats');
            }
        })
        .then(data => {
            // Process the fetched data (e.g., mark booked seats on the UI)
            console.log("MY NAME")
            console.log('Booked seats:', data);
            markBookedSeats(data.bookedSeats);
        })
        .catch(error => {
            console.error('Error fetching booked seats:', error.message);
        });
    }


    function fetchUsersBookedSeat() {
        const _date = urlParams.get('date');
        const route = urlParams.get('route_id');
        const userEmail = logged_in_user_email;

        fetch('/fetch-users-booked-seat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ _date: _date, route: route, userEmail: userEmail})
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error("Failed to fetch user's booked seat");
            }
        })
        .then(data => {
            // Process the fetched data (e.g., mark booked seats on the UI)
            console.log("Your Name")
            console.log('Booked seats:', data);
            displayBookedSeatNumber(data.bookedSeats);
        })
        .catch(error => {
            console.error('Error fetching booked seats:', error.message);
        });
    }

    function displayBookedSeatNumber(bookedSeat){
        if (bookedSeat.length>0){
            console.log("PLUOUS")
            allow = false
            const bookedDisplay = document.createElement('div');
            bookedDisplay.textContent = `You have booked seat number: ${bookedSeat[0]}`;
            bdisplay.appendChild(bookedDisplay);
        } else{
            console.log("ilgaa")
            allow = true
        }
    }
    // Function to mark booked seats on the UI
    function markBookedSeats(bookedSeats) {
        console.log(bookedSeats)
        console.log(bookedSeats.row)
        console.log(bookedSeats.seat)
        const seatElements = document.querySelectorAll('.seat');
        console.log(seatElements)
        seatElements.forEach(seatElement => {
            const row = seatElement.dataset.row;
            console.log(row)
            const seat = seatElement.dataset.seat;
            console.log(seat);
            var isBooked = false;

            for (const [key, bookedSeat] of Object.entries(bookedSeats)) {
                if (seat.length==3){
                    if (bookedSeat[0][0] == row && bookedSeat[0][2] == seat[0]){
                        isBooked=true;
                        break;
                    }
                } else {
                    if (bookedSeat[0][0] == row && bookedSeat[0][2] == seat[0] && bookedSeat[0][3] == seat[1]){
                        isBooked=true;
                        break;
                    }
                }
            }

            console.log(isBooked)
            if (isBooked) {
                seatElement.classList.add('booked');
            }
        });
        console.log("DINGA");
        const seatElementss = document.querySelectorAll('.centseat');
        seatElementss.forEach(seatElement =>{
            console.log(seatElement);
            const row = seatElement.dataset.row;
            console.log(row)
            const seat = seatElement.dataset.seat;
            console.log(seat)
            console.log("DINGA2");
            const isBooked = bookedSeats.some(bookedSeat => bookedSeat[0][0] == row && bookedSeat[0][2] == seat);
            console.log(isBooked)
            if (isBooked) {
                seatElement.classList.add('booked');
            }
            console.log("DINGA3");
        })

        const seatElementss2 = document.querySelectorAll('.centseat2');
        seatElementss2.forEach(seatElement =>{
            console.log(seatElement);
            const row = seatElement.dataset.row;
            console.log(row)
            const seat = seatElement.dataset.seat;
            console.log(seat)
            console.log("DINGA2");
            const isBooked = bookedSeats.some(bookedSeat => bookedSeat[0][0] == row && bookedSeat[0][2] == seat[0] &&bookedSeat[0][2] == seat[1]);
            console.log(isBooked)
            if (isBooked) {
                seatElement.classList.add('booked');
            }
            console.log("DINGA3");
        })
        // bookedSeats.forEach(bookedSeat=>{
        //     bookedSeat.classList.add('booked');
        // })
    }

    // Call the fetchBookedSeats function when the page loads
    fetchBookedSeats();
    fetchUsersBookedSeat();


    if (capacity==0){
        // Generate bus layout (assuming a 5x10 layout for demonstration)
        for (let row = 1; row <= 3; row++) {
            for (let seat = 1; seat <= 11; seat++) {
                const seatElement = document.createElement('div');
                seatElement.classList.add('seat');
                seatElement.dataset.row = row;
                seatElement.dataset.seat = seat;
                seatElement.textContent = `${row}-${seat}`;
                seatElement.addEventListener('click', toggleSeatSelection);
                busLayout.appendChild(seatElement);
            }
            busLayout.appendChild(document.createElement('br')); // Add line break after each row
        }
        for (let seat = 1; seat <= 10; seat++) {
            const seatElement = document.createElement('div');
            seatElement.classList.add('gap');
            seatElement.textContent = "_____________________";
            // seatElement.textContent = ".";
            busLayout.appendChild(seatElement);
        }
        const seatElement = document.createElement('div');
        seatElement.classList.add('centseat2');
        seatElement.dataset.row = 4;
        seatElement.dataset.seat = 11;
        seatElement.textContent = `${4}-${11}`;
        seatElement.addEventListener('click', toggleSeatSelection);
        busLayout.appendChild(seatElement);
        busLayout.appendChild(document.createElement('br')); // Add line break after each row
        for (let row = 5; row <= 6; row++) {
            for (let seat = 1; seat <= 11; seat++) {
                const seatElement = document.createElement('div');
                seatElement.classList.add('seat');
                seatElement.dataset.row = row;
                seatElement.dataset.seat = seat;
                seatElement.textContent = `${row}-${seat}`;
                seatElement.addEventListener('click', toggleSeatSelection);
                busLayout.appendChild(seatElement);
            }
            busLayout.appendChild(document.createElement('br')); // Add line break after each row
        }
    } else {
        // Generate bus layout (assuming a 5x10 layout for demonstration)
        for (let row = 1; row <= 2; row++) {
            for (let seat = 1; seat <= 7; seat++) {
                const seatElement = document.createElement('div');
                seatElement.classList.add('seat');
                seatElement.dataset.row = row;
                seatElement.dataset.seat = seat;
                seatElement.textContent = `${row}-${seat}`;
                seatElement.addEventListener('click', toggleSeatSelection);
                busLayout2.appendChild(seatElement);
            }
            busLayout2.appendChild(document.createElement('br')); // Add line break after each row
        }
        for (let seat = 1; seat <= 6; seat++) {
            const seatElement = document.createElement('div');
            seatElement.classList.add('gap');
            seatElement.textContent = "______________";
            busLayout2.appendChild(seatElement);
        }
        // busLayout2.appendChild(document.createElement('br')); // Add line break after each row
        const seatElement = document.createElement('div');
        seatElement.classList.add('centseat');
        seatElement.dataset.row = 3;
        seatElement.dataset.seat = 7;
        seatElement.textContent = `${3}-${7}`;
        seatElement.addEventListener('click', toggleSeatSelection);
        busLayout2.appendChild(seatElement);
        busLayout2.appendChild(document.createElement('br')); // Add line break after each row
        for (let row = 4; row <= 5; row++) {
            for (let seat = 1; seat <= 7; seat++) {
                const seatElement = document.createElement('div');
                seatElement.classList.add('seat');
                seatElement.dataset.row = row;
                seatElement.dataset.seat = seat;
                seatElement.textContent = `${row}-${seat}`;
                seatElement.addEventListener('click', toggleSeatSelection);
                busLayout2.appendChild(seatElement);
            }
            busLayout2.appendChild(document.createElement('br')); // Add line break after each row
        }
    }

    // Function to toggle seat selection
    function toggleSeatSelection(event) {
        const seatElement = event.target;
        const row = seatElement.dataset.row;
        const seat = seatElement.dataset.seat;
        const seatKey = `${row}-${seat}`;
        
        // Check if the seat is already selected
        if (selectedSeats.has(seatKey)) {
            selectedSeats.delete(seatKey);
            seatElement.classList.remove('selected');
        } else {
            // Check if the user has already booked a ticket
            console.log(allow)
            if (selectedSeats.size === 0 && allow) {
                if (!seatElement.classList.contains('booked')) { // Check if the seat is not booked
                    selectedSeats.add(seatKey);
                    seatElement.classList.add('selected');
                } else {
                    alert('This seat is already booked.');
                }    
            } else {
                alert('You can only book one ticket.');
            }
        }
    }

    // Function to handle booking button click
    function performBooking () {
        if (selectedSeats.size === 1) {
            // Convert selected seats set to an array
            const selectedSeatsArray = Array.from(selectedSeats);

            // Extract licence plate number from the URL
            const urlParams = new URLSearchParams(window.location.search);
            // const licencePlateNumber = urlParams.get('licence_plate_number');
            const _date = urlParams.get('date');
            const route = urlParams.get('route_id');

            // const userEmail = 'exampsfle_email@example.com'; 
            // const userEmail = session['emailID'];
            const userEmail = logged_in_user_email;


            // Send selected seats to server for booking
            fetch('/book-seats', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    selectedSeat: selectedSeatsArray[0],
                    // licencePlateNumber: licencePlateNumber,
                    userEmail: userEmail,
                    _date: _date,
                    route: route,
                })
            })
            .then(response => {
                if (response.ok) {
                    console.log("NOO")
                    return response.json();
                } else {
                    throw new Error('Failed to book seat');
                }
            })
            .then(data => {
                console.log("NAHHH")
                console.log('Booking successful:', data);
                // Optionally, display a success message to the user
                // location.reload();
                // alert("Booking Succesful!");
            })
            .catch(error => {
                // console.error('Error booking seat:', error.message);
                // Optionally, display an error message to the user


                // console.error('Error booking seat:', error.message);
                // // Show an alert if the user has already booked a ticket for this bus
                // location.reload();
                // alert('You have already booked a ticket for this bus.');

            });
            // fetchBookedSeats();
            // fetchUsersBookedSeat();
            // location.reload();
        } else {
            console.log("OOHHH")
            alert('Please select exactly one seat to book.');
        }
        // location.reload();
    };

    bookButton.addEventListener('click', function() {
        performBooking();
        fetchBookedSeats();
        fetchUsersBookedSeat();
        location.reload();
        alert("Booking Succesful!");
    });

        // Function to handle cancellation of booking
    function cancelBooking() {
        const urlParams = new URLSearchParams(window.location.search);
        // const licencePlateNumber = urlParams.get('licence_plate_number');
        // const emailId = 'exampsfle_email@example.com'; // You need to get the user's email ID somehow
        // const userEmail = session['emailID'];
        const userEmail = logged_in_user_email;


        const _date = urlParams.get('date');
        const route = urlParams.get('route_id');


        fetch('/cancel-booking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                _date: _date,
                route_id: route,
                emailId: userEmail
            })
        })
        .then(response => {
            if (response.ok) {
                console.log("Booking cancelled successfully");
                // alert("Booking cancelled successfully");
                // Update UI to mark cancelled seat as available
                // You may need additional logic here to find the seat number associated with the user's booking
            } else {
                console.log(response)
                throw new Error('Failed to cancel booking');
            }
        })
        .then(data => {
            // Extract the booked seat number from the response data
            const bookedSeat = data.canceledSeat;
            console.log(bookedSeat)
    
            // Update UI to mark the cancelled seat as available
            const seatElement = document.querySelector(`[data-seat="${bookedSeat}"]`);
            console.log(seatElement)
            if (seatElement) {
                seatElement.classList.remove('booked'); // Assuming 'booked' class marks a booked seat
            } else {
                console.error('Seat element not found:', bookedSeat);
            }
            
            console.log("Booking cancelled successfully");
        })
        .catch(error => {
            console.error('Error cancelling booking:', error.message);
            console.log('Error cancelling booking:', error.message);
            // Optionally, display an error message to the user
        });
    }

    cancelButton.addEventListener('click', function() {
        if (!allow){
            cancelBooking();
            fetchBookedSeats();
            fetchUsersBookedSeat();
            location.reload();
            alert("Booking cancelled successfully");
        } else {
            alert("You have not booked any seat yet");
        }
    });

});
