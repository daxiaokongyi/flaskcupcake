const BASE_URL = 'http://localhost:5000/api';

// Generate HTML for a cupcake with data
function generateCupcakeHTML(cupcake) {
    return `
        <div data-cupcake-id=${cupcake.id}>
            <li>
                ${cupcake.flavor}/${cupcake.size}/${cupcake.rating}
                <button class="btn btn-danger btn-sm delete-button">X</button>
            </li>
            <img class="img-thumbnail" src=${cupcake.image}>
        </div>
    `;
}

// Append a cupcake html to the cupcake list
async function getCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`)
    console.log(response)
    for (let each of response.data.cupcakes) {
        let newCupcake = generateCupcakeHTML(each)
        $("#cupcakes-list").append(newCupcake);
    }
}

// add a new cupcake on the form
$('#new-cupcake-form').on('submit', async function(event){
    event.preventDefault();
    let flavor = $('#flavor').val();
    let size = $('#size').val();
    let rating = $('#rating').val();
    let image = $('#image').val();

    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        size,
        rating,
        image
    });

    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $('#cupcakes-list').append(newCupcake);
    $('#new-cupcake-form').trigger("reset");
})

$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
    evt.preventDefault();
    console.log('hi')
    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});

$(getCupcakes);
