$(document).ready(function () {
    $("#chat-form").on("submit", function (event) {
        event.preventDefault();

        let user_message = $("#message-input").val();
        if (user_message.trim() === "") {
            alert("Please enter a message.");
            return;
        }

        // Append user message to the chat area
        $("#chat-area").append(`
            <div class="message user-message">
                <p>${user_message}</p>
            </div>
        `);

        // Clear the input field
        $("#message-input").val("");

        // Send the message to the server
        $.ajax({
            url: "/chat",  // Endpoint to handle the chatbot
            type: "POST",
            data: { msg: user_message },
            success: function (response) {
                // Append bot response to the chat area
                $("#chat-area").append(`
                    <div class="message bot-message">
                        <p>${response.response}</p>
                    </div>
                `);

                // If there are products, display them
                if (response.products && response.products.length > 0) {
                    let productHTML = '<div class="product-recommendations mt-4"><h4>Recommended Products</h4><div class="row">';
                    response.products.forEach(product => {
                        productHTML += `
                            <div class="col-md-4 mb-4">
                                <div class="card product-card">
                                    <img src="${product.image}" class="card-img-top" alt="${product.name}">
                                    <div class="card-body">
                                        <h5 class="card-title">${product.name}</h5>
                                        <p class="card-text">${product.price}</p>
                                        <a href="${product.link}" class="btn btn-primary" target="_blank">View Product</a>
                                        <p class="mt-2">Rating: ${product.rating} / 5</p>
                                    </div>
                                </div>
                            </div>
                        `;
                    });
                    productHTML += '</div></div>';

                    // Append product recommendations to the chat area
                    $("#chat-area").append(productHTML);
                }

                // Scroll to the bottom
                let chatArea = document.getElementById("chat-area");
                chatArea.scrollTop = chatArea.scrollHeight;
            },
            error: function () {
                alert("Error communicating with the server.");
            }
        });
    });
});
