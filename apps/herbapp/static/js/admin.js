(function($)
{
    $(document).ready(function($)
    {
        // based on plant type, display only relevant settings

		$("#id_plant_type").click(function(event) {
		    plant_type = $("#id_plant_type").val();
            switch (plant_type)
            {
                case "1":
                {
                    // plant
                    $("#fieldset-4").show(); // flower
                    $("#fieldset-5").show(); // leaf
                    $("#fieldset-6").hide(); // tree
                } break;

                case "2":
                {
                    // shrub
                    $("#fieldset-4").show(); // flower
                    $("#fieldset-5").show(); // leaf
                    $("#fieldset-6").show(); // tree
                    $(".field-needle_type").hide();
                    $(".field-branching").show();
                    $(".field-bark_type").hide();
                    $(".field-bark_type_alt").hide();
                } break;

                case "3":
                {
                    // needle tree
                    $("#fieldset-4").hide(); // flower
                    $("#fieldset-5").hide(); // leaf
                    $("#fieldset-6").show(); // tree
                    $(".field-needle_type").show();
                    $(".field-branching").hide();
                    $(".field-bark_type").show();
                    $(".field-bark_type_alt").show();
                } break;

                case "4":
                {
                    // leaf tree
                    $("#fieldset-4").show(); // flower
                    $("#fieldset-5").show(); // leaf
                    $("#fieldset-6").show(); // tree
                    $(".field-needle_type").hide();
                    $(".field-branching").show();
                    $(".field-bark_type").show();
                    $(".field-bark_type_alt").show();
                } break;
            }
		});


        // init fields
        $("#id_plant_type").css("background-color", "#f0f0a0").click();
        $("#id_botanical_name").css("font-weight", "bold");
    });

}) (django.jQuery);

