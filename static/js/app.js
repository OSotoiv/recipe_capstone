const $save_recipe = $('#save_recipe')
$save_recipe.on('click', saveRecipe)
const $saved_or_not = $('#saved_or_not')
const recipe_img = $('#recipe_img')
const ingredients_list = document.querySelectorAll('#ingredient')
function sayhi(e) {
    e.preventDefault;
    console.log('hi')
}
async function saveRecipe(e) {
    e.preventDefault();
    const recipe_id = $('#save_recipe').data('recipe_id');
    const recipe_title = $('#save_recipe').data('recipe_title');
    const ingredients_text = [];
    ingredients_list.forEach((item) => ingredients_text.push(item.innerText))
    try {
        const res = await axios({
            url: `http://127.0.0.1:5000/save_recipe/${recipe_id}/${recipe_title}`,
            method: "POST",
            data: { ingredients: ingredients_text, image: recipe_img[0].src }
        })
        if (res.data.response == 'unsaved') {
            $('#save_recipe').remove()
            $save_icon = $(`<button data-recipe_id=${recipe_id}
                            data-recipe_title=${recipe_title}
                            id="save_recipe" 
                            class="btn btn-primary btn-sm">
                            <i class="fa-regular fa-bookmark">
                            </i>Save to Cookbook</button>`)
            $save_icon.on('click', saveRecipe)
            $saved_or_not.append($save_icon)
        }
        else if (res.data.response == 'saved') {
            $('#save_recipe').remove()
            $save_icon = $(`<button data-recipe_id=${recipe_id}
                            data-recipe_title=${recipe_title}
                            id="save_recipe" 
                            class="btn btn-secondary btn-sm">
                            <i class="fa-solid fa-bookmark">
                            </i> SAVED</button>`)
            $save_icon.on('click', saveRecipe)
            $saved_or_not.append($save_icon)
        }
    } catch (error) {
        console.log(error)
    }
}