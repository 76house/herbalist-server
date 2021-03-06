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
                    $("#fieldset-6").show(); // flower
                    $("#fieldset-7").show(); // leaf
                    $("#fieldset-8").hide(); // shrub/tree
                    $(".field-leaf_arrangement").show();
                    $(".field-leaf_arrangement_alt").show();
                } break;

                case "2":
                {
                    // leaf shrub
                    $("#fieldset-6").show(); // flower
                    $("#fieldset-7").show(); // leaf
                    $("#fieldset-8").show(); // shrub/tree
                    $(".field-leaf_arrangement").hide();
                    $(".field-leaf_arrangement_alt").hide();
                    $(".field-needle_type").hide();
                    $(".field-branching").show();
                    $(".field-bark_type").hide();
                    $(".field-bark_type_alt").hide();
                } break;

                case "3":
                {
                    // needle shrub
                    $("#fieldset-6").hide(); // flower
                    $("#fieldset-7").hide(); // leaf
                    $("#fieldset-8").show(); // shrub/tree
                    $(".field-leaf_arrangement").hide();
                    $(".field-leaf_arrangement_alt").hide();
                    $(".field-needle_type").show();
                    $(".field-branching").hide();
                    $(".field-bark_type").hide();
                    $(".field-bark_type_alt").hide();
                } break;

                case "4":
                {
                    // leaf tree
                    $("#fieldset-6").show(); // flower
                    $("#fieldset-7").show(); // leaf
                    $("#fieldset-8").show(); // shrub/tree
                    $(".field-leaf_arrangement").hide();
                    $(".field-leaf_arrangement_alt").hide();
                    $(".field-needle_type").hide();
                    $(".field-branching").show();
                    $(".field-bark_type").show();
                    $(".field-bark_type_alt").show();
                } break;

                case "5":
                {
                    // needle tree
                    $("#fieldset-6").hide(); // flower
                    $("#fieldset-7").hide(); // leaf
                    $("#fieldset-8").show(); // shrub/tree
                    $(".field-leaf_arrangement").hide();
                    $(".field-leaf_arrangement_alt").hide();
                    $(".field-needle_type").show();
                    $(".field-branching").hide();
                    $(".field-bark_type").show();
                    $(".field-bark_type_alt").show();
                } break;
            }
		});

		$("#id_leaf_type").click(function(event) {
		    leaf_type = $("#id_leaf_type").val();
		    if (leaf_type == 2 || leaf_type == 3 || leaf_type == 7) {
		        $(".field-leaf_shape").hide();
		        $(".field-leaf_shape_alt").hide();
            } else {
                $(".field-leaf_shape").show();
                $(".field-leaf_shape_alt").show();
            }
		});


        // init fields
        $("#id_plant_type").css("background-color", "#f0f0a0").click();
        $("#id_leaf_type").click();
        $("#id_botanical_name").css("font-weight", "bold");
        $(".field-is_draft").css("margin-bottom", "40px");
        $(".field-is_draft label")
            .css("color", "#fff")
            .css("background", "#5c9425")
            .css("padding", "0.1em 0.3em")
            .css("border-radius", "3px")
            .css("width", "3.5em")
            .css("font-size", "0.9em")
            .css("text-transform", "uppercase");
    });

}) (django.jQuery);

