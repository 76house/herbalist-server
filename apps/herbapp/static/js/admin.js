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
                    $(".field-leaf_arrangement").show();
                    $(".field-leaf_arrangement_alt").show();
                } break;

                case "2":
                {
                    // leaf shrub
                    $("#fieldset-5").show(); // flower
                    $("#fieldset-6").show(); // leaf
                    $("#fieldset-7").show(); // shrub/tree
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
                    $("#fieldset-5").hide(); // flower
                    $("#fieldset-6").hide(); // leaf
                    $("#fieldset-7").show(); // shrub/tree
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
                    $("#fieldset-5").show(); // flower
                    $("#fieldset-6").show(); // leaf
                    $("#fieldset-7").show(); // shrub/tree
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
                    $("#fieldset-5").hide(); // flower
                    $("#fieldset-6").hide(); // leaf
                    $("#fieldset-7").show(); // shrub/tree
                    $(".field-leaf_arrangement").hide();
                    $(".field-leaf_arrangement_alt").hide();
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
        $(".field-is_draft label")
          .css("color", "#fff")
          .css("background", "#5c9425")
          .css("padding", "0.1em 0.3em")
          .css("float", "right")
          .css("border-radius", "3px")
          .css("font-size", "0.9em")
          .css("text-transform", "uppercase");
    });

}) (django.jQuery);

