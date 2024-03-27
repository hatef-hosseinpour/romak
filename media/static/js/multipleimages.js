$(document).ready(function () {
    imgUpload();
});

function imgUpload() {
    let imgWarp = "";
    let imgArray = [];
    $(".upload-inputfile").each(function () {
        $(this).on('change', function (e) {
            imgWarp = $(this).closest('.upload-box').find('.upload--img-wrap');
            let maxLength = $(this).attr('data-max-length');

            let files = e.target.files;
            let filesArr = Array.prototype.slice.call(files);
            let iterator = 0;
            filesArr.forEach(function (f, index) {
                if (!f.type.match('image.*')) {
                    return;
                }
                if (imgArray.length > maxLength) {
                    return false;
                } else {
                    let len = 0;
                    for (let i = 0; i < imgArray.length; i++) {
                        if (imgArray[i] != undefined) {
                            len++;
                        }
                    }
                    if (len > maxLength) {
                        return false;
                    }
                    else {
                        imgArray.push(f);
                        let reader = new FileReader();
                        reader.onload = function (e) {
                            let html = "<div class='upload-img-box'><div style='background-image: url(" + e.target.result + ")' data-number='" + $(".upload-img-close").length + "' data-file='" + f.name + "' class='img-bg'><div class='upload-img-close' id=></div></div></div>";
                            imgWarp.append(html);
                            iterator++;
                        }
                        reader.readAsDataURL(f)

                    }
                }
            });

        });
    });
    $('.form-control').on('click', ".upload-img-close", function (e) {
        let file = $(this).parent().data("file");

        for (let i = 0; i < imgArray.length; i++) {
            if (imgArray.name === file) {
                imgArray.slice(i, 1);
                break;
            }
        }
        console.log(imgArray);
        $(this).parent().parent().remove();
    });
}