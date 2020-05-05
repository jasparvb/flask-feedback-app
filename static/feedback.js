const BASE_URL = "http://127.0.0.1:5000/api";

class Cupcakes {
    constructor() {
        this.getCupcakes()
        $('#add-cupcake-form').on('submit', this.addCupcake.bind(this))
        $('#cupcake-list').on('click', '.delete-btn', this.deleteCupcake.bind(this))
    }

    async getCupcakes() {
        const response = await axios.get(`${BASE_URL}/cupcakes`);
        for(let cupcake of response.data.cupcakes) {
            this.generateHTML(cupcake);
        }
    }
    
    generateHTML(cupcake) {
        let $item = $(`
            <li>
                <img class="" src="${cupcake.image}">
                <p>Flavor: ${cupcake.flavor}<br>
                Size: ${cupcake.size}<br>
                Rating: ${cupcake.rating}</p>
                <button data-id="${cupcake.id}" class="delete-btn">Delete</button>
            </li>
        `);
        $('#cupcake-list').append($item);
    }

    async addCupcake(e) {
        e.preventDefault();
        let flavor = $('#flavor').val();
        let size = $('#size').val();
        let rating = $('#rating').val();
        let image = $('#image').val();
        const response = await axios.post(`${BASE_URL}/cupcakes`, {flavor, size, rating, image});

        this.generateHTML(response.data.cupcake);
        $("#add-cupcake-form").trigger("reset");
    }

    async deleteCupcake(e) {
        let cupcakeId = $(e.target).attr('data-id');
        await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
        $(e.target).closest('li').remove();
    }
}

$(async function() {
    //new Cupcakes();
});