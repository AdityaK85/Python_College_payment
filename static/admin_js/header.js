window.handleLiveData = function (live_data_web) {
    if ("nfty_idx" in live_data_web) {
        var nfty_ltp = live_data_web['nfty_idx'];
        var bnk_ltp = live_data_web['bnfty_idx'];
        var nft_LTP = nfty_ltp['lp']
        var bnft_LTP = bnk_ltp['lp']
        $("#nfty_prc").html(`<span class="mx-2">${nft_LTP}</span> <small class="mx-3 ${nfty_ltp['pc'] > 0 ? 'text-success' : 'text-danger' }" >${nfty_ltp['pc']}%</small><i class="fas fa-${nfty_ltp['pc'] > 0 ? 'angle-up  text-success' : 'angle-down  text-danger' }"></i> ` )
        $("#nfy_open_price").html( nfty_ltp['o'])
        $("#nfy_high_price").html( nfty_ltp['h'])
        $("#nfy_low_price").html( nfty_ltp['l'])
        $("#nfy_close_price").html( nfty_ltp['c'])
        
        $("#bnknfty_prc").html(`<span class="mx-2">${bnft_LTP}</span> <small class="mx-3 ${bnk_ltp['pc'] > 0 ? 'text-success' : 'text-danger' } ">${bnk_ltp['pc']}%</small><i class="fas fa-${bnk_ltp['pc'] > 0 ? 'angle-up  text-success' : 'angle-down  text-danger' }"></i> `)
        $("#bnfnty_open_price").html( bnk_ltp['o'])
        $("#bnfnty_high_price").html( bnk_ltp['h'])
        $("#bnfnty_low_price").html( bnk_ltp['l'])
        $("#bnfnty_close_price").html( bnk_ltp['c'])
    }
}