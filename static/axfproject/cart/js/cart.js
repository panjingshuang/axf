$(document).ready(function(){

    //修改购物车
    var subShoppings = document.getElementsByClassName('subShopping')
    var addShoppings = document.getElementsByClassName('addShopping')


    for (var i=0;i<addShoppings.length;i++){
       var  addShopping =  addShoppings[i]
        addShopping.addEventListener('click',function () {
            pid = this.getAttribute('ga')
            $.post('/changecart/0/',{'productid':pid},function (data) {

                if(data.data == -1) {
                    window.location.href = 'http://127.0.0.1:8001/login/'
                }else if (data.data==0){
                    document.getElementById(pid).innerHTML = data.number
                    document.getElementById(pid+'price').innerHTML = data.price
                }
            })
        },false)

    }


     for (var i=0;i<subShoppings.length;i++){
       var  subShopping =  subShoppings[i]
        subShopping.addEventListener('click',function () {
            pid = this.getAttribute('ga')
            $.post('/changecart/1/',{'productid':pid},function (data) {
                if(data.data == -1) {
                    window.location.href = 'http://127.0.0.1:8001/login/'
                }else if(data.data == 1){
                    if(data.number == 0){
                        var li  =   document.getElementById(pid+'li')
                         li.parentNode.removeChild(li)
                    }else{
                        document.getElementById(pid).innerHTML = data.number
                        document.getElementById(pid+'price').innerHTML = data.price
                    }
                }

            })
        },false)

    }





     var ischoses =  document.getElementsByClassName('ischose')

    var count = 0;
     for (var i=0;i<ischoses.length;i++){
       var  ischose =  ischoses[i]
        ischose.addEventListener('click',function () {
            pid = this.getAttribute('goodsid')
            $.post('/changecart/2/',{'productid':pid},function (data) {
                if(data.data == -1) {
                    window.location.href = 'http://127.0.0.1:8001/login/'
                }else if(data.data == 2){
                     document.getElementById(pid+'a').innerHTML = data.ischose
                   if(data.search_all == 1){
                         document.getElementById('confim_all').innerHTML = '√'
                   }else{
                         document.getElementById('confim_all').innerHTML = ''
                   }
                }

            })


        },false)
    }
    
    
    var ok  = document.getElementById('ok')
    ok.addEventListener('click',function () {
            var f  = confirm('是否确定要下订单？')
            if(f){
                $.post('/saveorder/',function (data) {
                   if(data.data == -1) {
                    window.location.href = 'http://127.0.0.1:8001/login/'
                }else if(data.status=='success'){
                     window.location.href = "http://127.0.0.1:8001/cart/"
                   }
                })
            }

    })



















    
    




})