function printCatchTable() {
    var $table = $('#TableLastCaught');

    $.ajax({
                type: "GET",
                url: '/api/lastcaught',
                success: function(response) {

                    for (var i = 0; i < response.length; i++) {
                        var item = response[i];
                        var picinfos = item.picinfos;

                        for (var x in picinfos) {
                            var filename = picinfos[x].filename;
                        }

                        faengeTableData.push({
                                _id: item._id,
                                date: item.datum,
                                time: item.uhrzeit,
                                pics: filename,
                            })

                            $table.bootstrapTable({
                                data: faengeTableData
                            }); $table.bootstrapTable('togglePagination');
                        }
                    }


            }(

            function imageFormatter(value, row) {
                return '<img src="files/' + value + '" />';
            })