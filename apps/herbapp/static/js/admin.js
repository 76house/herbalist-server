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
                    $("#fieldset-5").show(); // flower
                    $("#fieldset-6").show(); // leaf
                    $("#fieldset-7").hide(); // shrub/tree
                } break;

                case "2":
                {
                    // leaf shrub
                    $("#fieldset-5").show(); // flower
                    $("#fieldset-6").show(); // leaf
                    $("#fieldset-7").show(); // shrub/tree
                    $(".field-needle_type").hide();
                    $(".field-branching").show();
                    $(".field-bark_type").hide();
                    $(".field-bark_type_alt").hide();
                } break;

                case "3":
                {
                    // needle shrub
                    $("#fieldset-5").hide(); // flower
                    $("#fieldset-6").hide(); // leaf
                    $("#fieldset-7").show(); // shrub/tree
                    $(".field-needle_type").show();
                    $(".field-branching").hide();
                    $(".field-bark_type").hide();
                    $(".field-bark_type_alt").hide();
                } break;

                case "4":
                {
                    // leaf tree
                    $("#fieldset-5").show(); // flower
                    $("#fieldset-6").show(); // leaf
                    $("#fieldset-7").show(); // shrub/tree
                    $(".field-needle_type").hide();
                    $(".field-branching").show();
                    $(".field-bark_type").show();
                    $(".field-bark_type_alt").show();
                } break;

                case "5":
                {
                    // needle tree
                    $("#fieldset-5").hide(); // flower
                    $("#fieldset-6").hide(); // leaf
                    $("#fieldset-7").show(); // shrub/tree
                    $(".field-needle_type").show();
                    $(".field-branching").hide();
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

