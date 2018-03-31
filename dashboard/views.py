from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .forms import CountryForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .decorators import isKYCverified,isAdminUser
from .models import KYCdata, keychain
from .forms import KYCForm
from django.views.decorators.cache import never_cache
from django.views.generic import FormView, TemplateView
from two_factor.views import OTPRequiredMixin
from two_factor.views.utils import class_view_decorator
from coinmarketcap import Market
from pycoin.cmds import ku
from pycoin.tx import tx_utils as txu
from pycoin.cmds import tx
from pycoin.version import version
from django.http import JsonResponse
import math
import decimal
import os
import simplejson
from .utils import get_country

name_to_numeric = {
"Aruba":"533",
"Afghanistan":"004",
"Angola":"024",
"Anguilla":"660",
"Åland Islands":"248",
"Albania":"008",
"Andorra":"020",
"United Arab Emirates":"784",
"Argentina":"032",
"Armenia":"051",
"American Samoa":"016",
"Antarctica":"010",
"French Southern Territories":"260",
"Antigua and Barbuda":"028",
"Australia":"036",
"Austria":"040",
"Azerbaijan":"031",
"Burundi":"108",
"Belgium":"056",
"Benin":"204",
"Bonaire, Sint Eustatius and Saba":"535",
"Burkina Faso":"854",
"Bangladesh":"050",
"Bulgaria":"100",
"Bahrain":"048",
"Bahamas":"044",
"Bosnia and Herzegovina":"070",
"Saint Barthélemy":"652",
"Belarus":"112",
"Belize":"084",
"Bermuda":"060",
"Bolivia, Plurinational State of":"068",
"Brazil":"076",
"Barbados":"052",
"Brunei Darussalam":"096",
"Bhutan":"064",
"Bouvet Island":"074",
"Botswana":"072",
"Central African Republic":"140",
"Canada":"124",
"Cocos (Keeling) Islands":"166",
"Switzerland":"756",
"Chile":"152",
"China":"156",
"Côte d'Ivoire":"384",
"Cameroon":"120",
"Congo, The Democratic Republic of the":"180",
"Congo":"178",
"Cook Islands":"184",
"Colombia":"170",
"Comoros":"174",
"Cabo Verde":"132",
"Costa Rica":"188",
"Cuba":"192",
"Curaçao":"531",
"Christmas Island":"162",
"Cayman Islands":"136",
"Cyprus":"196",
"Czechia":"203",
"Germany":"276",
"Djibouti":"262",
"Dominica":"212",
"Denmark":"208",
"Dominican Republic":"214",
"Algeria":"012",
"Ecuador":"218",
"Egypt":"818",
"Eritrea":"232",
"Western Sahara":"732",
"Spain":"724",
"Estonia":"233",
"Ethiopia":"231",
"Finland":"246",
"Fiji":"242",
"Falkland Islands (Malvinas)":"238",
"France":"250",
"Faroe Islands":"234",
"Micronesia, Federated States of":"583",
"Gabon":"266",
"United Kingdom":"826",
"Georgia":"268",
"Guernsey":"831",
"Ghana":"288",
"Gibraltar":"292",
"Guinea":"324",
"Guadeloupe":"312",
"Gambia":"270",
"Guinea-Bissau":"624",
"Equatorial Guinea":"226",
"Greece":"300",
"Grenada":"308",
"Greenland":"304",
"Guatemala":"320",
"French Guiana":"254",
"Guam":"316",
"Guyana":"328",
"Hong Kong":"344",
"Heard Island and McDonald Islands":"334",
"Honduras":"340",
"Croatia":"191",
"Haiti":"332",
"Hungary":"348",
"Indonesia":"360",
"Isle of Man":"833",
"India":"356",
"British Indian Ocean Territory":"086",
"Ireland":"372",
"Iran, Islamic Republic of":"364",
"Iraq":"368",
"Iceland":"352",
"Israel":"376",
"Italy":"380",
"Jamaica":"388",
"Jersey":"832",
"Jordan":"400",
"Japan":"392",
"Kazakhstan":"398",
"Kenya":"404",
"Kyrgyzstan":"417",
"Cambodia":"116",
"Kiribati":"296",
"Saint Kitts and Nevis":"659",
"Korea, Republic of":"410",
"Kuwait":"414",
"Lao People's Democratic Republic":"418",
"Lebanon":"422",
"Liberia":"430",
"Libya":"434",
"Saint Lucia":"662",
"Liechtenstein":"438",
"Sri Lanka":"144",
"Lesotho":"426",
"Lithuania":"440",
"Luxembourg":"442",
"Latvia":"428",
"Macao":"446",
"Saint Martin (French part)":"663",
"Morocco":"504",
"Monaco":"492",
"Moldova, Republic of":"498",
"Madagascar":"450",
"Maldives":"462",
"Mexico":"484",
"Marshall Islands":"584",
"Macedonia, Republic of":"807",
"Mali":"466",
"Malta":"470",
"Myanmar":"104",
"Montenegro":"499",
"Mongolia":"496",
"Northern Mariana Islands":"580",
"Mozambique":"508",
"Mauritania":"478",
"Montserrat":"500",
"Martinique":"474",
"Mauritius":"480",
"Malawi":"454",
"Malaysia":"458",
"Mayotte":"175",
"Namibia":"516",
"New Caledonia":"540",
"Niger":"562",
"Norfolk Island":"574",
"Nigeria":"566",
"Nicaragua":"558",
"Niue":"570",
"Netherlands":"528",
"Norway":"578",
"Nepal":"524",
"Nauru":"520",
"New Zealand":"554",
"Oman":"512",
"Pakistan":"586",
"Panama":"591",
"Pitcairn":"612",
"Peru":"604",
"Philippines":"608",
"Palau":"585",
"Papua New Guinea":"598",
"Poland":"616",
"Puerto Rico":"630",
"Korea, Democratic People's Republic of":"408",
"Portugal":"620",
"Paraguay":"600",
"Palestine, State of":"275",
"French Polynesia":"258",
"Qatar":"634",
"Réunion":"638",
"Romania":"642",
"Russian Federation":"643",
"Rwanda":"646",
"Saudi Arabia":"682",
"Sudan":"729",
"Senegal":"686",
"Singapore":"702",
"South Georgia and the South Sandwich Islands":"239",
"Saint Helena, Ascension and Tristan da Cunha":"654",
"Svalbard and Jan Mayen":"744",
"Solomon Islands":"090",
"Sierra Leone":"694",
"El Salvador":"222",
"San Marino":"674",
"Somalia":"706",
"Saint Pierre and Miquelon":"666",
"Serbia":"688",
"South Sudan":"728",
"Sao Tome and Principe":"678",
"Suriname":"740",
"Slovakia":"703",
"Slovenia":"705",
"Sweden":"752",
"Swaziland":"748",
"Sint Maarten (Dutch part)":"534",
"Seychelles":"690",

"Turks and Caicos Islands":"796",
"Chad":"148",
"Togo":"768",
"Thailand":"764",
"Tajikistan":"762",
"Tokelau":"772",
"Turkmenistan":"795",
"Timor-Leste":"626",
"Tonga":"776",
"Trinidad and Tobago":"780",
"Tunisia":"788",
"Turkey":"792",
"Tuvalu":"798",
"Taiwan, Province of China":"158",
"Tanzania, United Republic of":"834",
"Uganda":"800",
"Ukraine":"804",
"United States Minor Outlying Islands":"581",
"Uruguay":"858",
"United States":"840",
"Uzbekistan":"860",
"Holy See (Vatican City State)":"336",
"Saint Vincent and the Grenadines":"670",
"Venezuela, Bolivarian Republic of":"862",
"Virgin Islands, British":"092",
"Virgin Islands, U.S.":"850",
"Viet Nam":"704",
"Vanuatu":"548",
"Wallis and Futuna":"876",
"Samoa":"882",
"Yemen":"887",
"South Africa":"710",
"Zambia":"894",
"Zimbabwe":"716",
}

numeric_to_currency = {
"784":"AED" ,
"971":"AFN" ,
"008":"ALL" ,
"051":"AMD" ,
"532":"ANG" ,
"973":"AOA" ,
"032":"ARS" ,
"036":"AUD" ,
"533":"AWG" ,
"944":"AZN" ,
"977":"BAM" ,
"052":"BBD" ,
"050":"BDT" ,
"975":"BGN" ,
"048":"BHD" ,
"108":"BIF" ,
"060":"BMD" ,
"096":"BND" ,
"068":"BOB" ,
"986":"BRL" ,
"044":"BSD" ,
"064":"BTN" ,
"072":"BWP" ,
"933":"BYN" ,
"084":"BZD" ,
"124":"CAD" ,
"976":"CDF" ,
"756":"CHF" ,
"152":"CLP" ,
"156":"CNY" ,
"170":"COP" ,
"188":"CRC" ,
"931":"CUC" ,
"192":"CUP" ,
"132":"CVE" ,
"203":"CZK" ,
"262":"DJF" ,
"208":"DKK" ,
"214":"DOP" ,
"012":"DZD" ,
"818":"EGP" ,
"232":"ERN" ,
"230":"ETB" ,
"978":"EUR" ,
"242":"FJD" ,
"238":"FKP" ,
"826":"GBP" ,
"981":"GEL" ,
"936":"GHS" ,
"292":"GIP" ,
"270":"GMD" ,
"324":"GNF" ,
"320":"GTQ" ,
"328":"GYD" ,
"344":"HKD" ,
"340":"HNL" ,
"191":"HRK" ,
"332":"HTG" ,
"348":"HUF" ,
"360":"IDR" ,
"376":"ILS" ,
"356":"INR" ,
"368":"IQD" ,
"364":"IRR" ,
"352":"ISK" ,
"388":"JMD" ,
"400":"JOD" ,
"392":"JPY" ,
"404":"KES" ,
"417":"KGS" ,
"116":"KHR" ,
"174":"KMF" ,
"408":"KPW" ,
"410":"KRW" ,
"414":"KWD" ,
"136":"KYD" ,
"398":"KZT" ,
"418":"LAK" ,
"422":"LBP" ,
"144":"LKR" ,
"430":"LRD" ,
"426":"LSL" ,
"434":"LYD" ,
"504":"MAD" ,
"498":"MDL" ,
"969":"MGA" ,
"807":"MKD" ,
"104":"MMK" ,
"496":"MNT" ,
"446":"MOP" ,
"478":"MRO" ,
"480":"MUR" ,
"462":"MVR" ,
"454":"MWK" ,
"484":"MXN" ,
"458":"MYR" ,
"943":"MZN" ,
"516":"NAD" ,
"566":"NGN" ,
"558":"NIO" ,
"578":"NOK" ,
"524":"NPR" ,
"554":"NZD" ,
"512":"OMR" ,
"590":"PAB" ,
"604":"PEN" ,
"598":"PGK" ,
"608":"PHP" ,
"586":"PKR" ,
"985":"PLN" ,
"600":"PYG" ,
"634":"QAR" ,
"946":"RON" ,
"941":"RSD" ,
"643":"RUB" ,
"646":"RWF" ,
"682":"SAR" ,
"090":"SBD" ,
"690":"SCR" ,
"938":"SDG" ,
"752":"SEK" ,
"702":"SGD" ,
"654":"SHP" ,
"694":"SLL" ,
"706":"SOS" ,
"968":"SRD" ,
"728":"SSP" ,
"678":"STD" ,
"222":"SVC" ,

"748":"SZL" ,
"764":"THB" ,
"972":"TJS" ,
"934":"TMT" ,
"788":"TND" ,
"776":"TOP" ,
"949":"TRY" ,
"780":"TTD" ,
"901":"TWD" ,
"834":"TZS" ,
"980":"UAH" ,
"800":"UGX" ,
"840":"USD" ,
"858":"UYU" ,
"860":"UZS" ,
"937":"VEF" ,
"704":"VND" ,
"548":"VUV" ,
"882":"WST" ,
"950":"XAF" ,
"961":"XAG" ,
"959":"XAU" ,
"955":"XBA" ,
"956":"XBB" ,
"957":"XBC" ,
"958":"XBD" ,
"951":"XCD" ,
"960":"XDR" ,
"952":"XOF" ,
"964":"XPD" ,
"953":"XPF" ,
"962":"XPT" ,
"994":"XSU" ,
"963":"XTS" ,
"965":"XUA" ,
"999":"XXX" ,
"886":"YER" ,
"710":"ZAR" ,
"967":"ZMW" ,
"932":"ZWL" ,

}

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



@isAdminUser
def admin_image(request):
    user_pan = KYCdata.objects.values_list('PAN', flat=True)
    user_aadhaar = KYCdata.objects.values_list('aadhaar', flat=True)
    usern = KYCdata.objects.values_list('user', flat=True)
    return render(request,'dashboard/admin_image_view.html',{"user_pan":user_pan,"user_aadhaar":user_aadhaar,"usern":usern})

def serve_ajax_request(request):
    ip = get_client_ip(request)
    coinmarketcap = Market()
    coin = ["litecoin","dash"]
    country = get_country(str('202.141.80.30')) #in deployement case put variable ip here
    curr = numeric_to_currency[name_to_numeric[str(country)]].lower()
    result_list = []
    for co in coin: 
        if curr == 'eur':
            response = coinmarketcap.ticker(co,convert=curr)
            result = { "coin":response[0]["symbol"],
            "currency":curr.upper(),
            "buyrate":math.ceil((decimal.Decimal(response[0]["price_%s"%(curr)])+decimal.Decimal(1000.00/85.35))*10/10),
            "sellrate":math.ceil((decimal.Decimal(response[0]["price_%s"%(curr)])-decimal.Decimal(1000.00/85.35))*10/10)} #dollor value
        elif curr == 'inr':
            response = coinmarketcap.ticker(co,convert=curr)
            result = { "coin":response[0]["symbol"],
            "currency":curr.upper(),
            "buyrate":math.ceil((decimal.Decimal(response[0]["price_%s"%(curr)])+decimal.Decimal(1000.00))*10/10),
            "sellrate":math.ceil((decimal.Decimal(response[0]["price_%s"%(curr)])-decimal.Decimal(1000.00))*10/10)}
        elif curr == numeric_to_currency[name_to_numeric['Singapore']].lower():   
            response = coinmarketcap.ticker(co,convert=curr)
            result = { "coin":response[0]["symbol"],
            "currency":'SGD',
            "buyrate":math.ceil((decimal.Decimal(response[0]["price_%s"%(curr)])+decimal.Decimal(1000.00/49.61))*10/10),
            "sellrate":math.ceil((decimal.Decimal(response[0]["price_%s"%(curr)])-decimal.Decimal(1000.00/49.61))*10/10)} 
        else:
            response = coinmarketcap.ticker(co,convert='USD')
            result = { "coin":response[0]["symbol"],
            "currency":'USD',
            "buyrate":math.ceil((decimal.Decimal(response[0]["price_%s"%(curr)])+decimal.Decimal(1000.00/65.02))*10/10),
            "sellrate":math.ceil((decimal.Decimal(response[0]["price_%s"%(curr)])-decimal.Decimal(1000.00/65.02))*10/10)} #dollor value
        result_list.append(result) 
    return HttpResponse(simplejson.dumps(result_list))            

def index(request):
    ip = get_client_ip(request)
    #print(get_country(str('202.141.80.30')))
    coinmarketcap = Market()
    coin = "bitcoin"
    country = get_country(str('202.141.80.30')) #in deployement case put variable ip here
    curr = numeric_to_currency[name_to_numeric[str(country)]].lower()
    #["usd","inr","eur"]
    response = coinmarketcap.ticker(coin,convert=curr)
    result_list=[]
    result = {"coin":response[0]["symbol"],
    "currency":curr.upper(),
    "buyrate":math.ceil((decimal.Decimal(response[0]["price_%s"%(curr)])+decimal.Decimal(10000.00))*10/10),
    "sellrate":math.ceil((decimal.Decimal(response[0]["price_%s"%(curr)])-decimal.Decimal(10000.00))*10/10)} #dollor value
    result_list.append(result)
    return render(request, 'dashboard/index.html',{"result_list":result_list})
               
def blog(request):
    return render(request, 'dashboard/blog.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            form.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Rubit account.'
            message = render_to_string('dashboard/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request,'dashboard/emailsendpop.html')
    else:
        form = SignUpForm()
    return render(request, 'dashboard/register.html', {'form': form})

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)
    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request,'dashboard/conf_emailpop.html')
    else:
        return HttpResponse('Activation link is invalid!')    


def country(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            countries = form.cleaned_data.get('countries')
            # do something with your results
    else:
        form = CountryForm

    return render(request,'dashboard/country.html', {'form':form })      


def kyc_upload(request):
    try:
        profile = request.user.kycdata
    except KYCdata.DoesNotExist:
        profile = KYCdata(user=request.user)
    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, 'dashboard/home.html', {
                'form': form
            })
    else:
        form = KYCForm()
    return render(request, 'dashboard/kyc_form_upload.html', {
        'form': form
    })


def check_balance(spender_address, network):
    spends = tx.spendables_for_address(spender_address, network)
    try:
        balance = spends[0].coin_value
    except:
        if len(spends) == 0:
            return 0,0
    print("Balance in the account %s --> %s satoshis" % (spender_address, balance))
    return balance, spends


def sendCryptos(username, recipient_address, network, value):
    userdetails = keychain.objects.filter(username=username, network=network)[0]
    spender_address = userdetails.coinAddress
    private_key = userdetails.private_key
    to_send = value
    miner_fee = 12000
    comm_amount_in_satoshis = 500
    comm_wallet_address = ""
    if network == "LTC":
        miner_fee = 20000
        comm_amount_in_satoshis = 40000
        comm_wallet_address = ""
    elif network == "DASH":
        miner_fee = 100000
        comm_amount_in_satoshis = 250000
        comm_wallet_address = ""
    PYCOIN_AGENT = 'pycoin/%s' % version

    balance, spends = check_balance(spender_address, network)

    send_back = balance - miner_fee - comm_amount_in_satoshis - to_send

    if send_back > 0:
        transaction = txu.create_tx(spends, [(recipient_address, to_send), (spender_address, send_back), \
                                             (comm_wallet_address, comm_amount_in_satoshis)])
        txu.sign_tx(transaction, wifs=[private_key])

        hex_of_trans = transaction.as_hex()

        url = "https://api.blockcypher.com/v1/" + network.lower() + "/main/txs/push"
        payload = {"tx": hex_of_trans}
        headers = {'content-type': 'application/json', 'User-agent': PYCOIN_AGENT}
        result = requests.post(url, data=json.dumps(payload).encode("utf8"), headers=headers)
        print(result.content.decode("utf8"))
        send_receives.objects.create(username=username, network=network, type = 'send',
                                     other_user = recipient_address, value = to_send)
        return result.content.decode("utf8")

    else:
        print("Not enough balance")
        return 'Not enough balance'


def send(request):
    if request.user.username:
        if request.method == 'POST':
            # print("post")
            try:
                data=request.POST
                value= int(float(data['value'])*100000000)
                recipient_address = data['recp_addr']
                username = request.user.username
                network = data['network']
                print("######## Send Attempted ##########")
                print(value)
                print(recipient_address)
                print(username)
                print(network)
                print('Output :')
                output = sendCryptos(username, recipient_address, network, value)
                print("#################################")
                return HttpResponse('<html><h1>Send Attempted. '+str(output)+'</h1></html>')
            except Exception as e:
                return redirect('dashboard')

        else:
            print("not post")
            return redirect('dashboard')


@isKYCverified
def dashboard(request):
    session = request.session
    print(session) #session IP
    user = request.user
    user_obj = KYCdata.objects.get(user=user)
    if not user_obj.key_generated:
        networks = 'BTC','LTC','DASH'
        for network in networks:
            randomkey = ku.BIP32Node.from_master_secret(os.urandom(64), netcode=network)
            address = randomkey.address()
            pub_x, pub_y = randomkey.public_pair()
            priv = randomkey.wif()
            sec = randomkey.sec_as_hex()
            keychain.objects.create(username=user.username, network=network, public_key_x=pub_x, public_key_y=pub_y, \
                                    private_key=priv, sec=sec, coinAddress=address)
            user_obj.key_generated = True
            user_obj.save()

            print('keychain created for user :' + user.username + ', on network: ' + network)
    
    username = request.user.username
    keys = keychain.objects.filter(username=username)
    ltc_key = keys.get(network = 'LTC').coinAddress
    btc_key = keys.get(network='BTC').coinAddress
    dash_key = keys.get(network='DASH').coinAddress

    btc_balance = check_balance(btc_key, 'BTC')
    ltc_balance = check_balance(ltc_key, 'LTC')
    dash_balance = check_balance(dash_key, 'DASH')

    # print('BTC Balance and Spends: %d, %d'%(btc_balance[0],ltc_balance[1]))
    # print('LTC Balance and Spends: %d, %d'%(ltc_balance[0],ltc_balance[1]))
    # print('DASH Balance and Spends: %d, %d'%(dash_balance[0],ltc_balance[1]))
    
    data = {
    "ltc_key" : ltc_key,
    "btc_key" : btc_key,
    "dash_key" : dash_key,
    "btc_balance" : btc_balance[0]/100000000,
    "ltc_balance" : ltc_balance[0]/100000000,
    "dash_balance" : dash_balance[0]/100000000,
    }
    return render(request, 'dashboard/dashboard.html', data)

@isKYCverified
def two_factor(request): 
    return redirect('account/two_factor')

@class_view_decorator(never_cache)
class ExampleSecretView(OTPRequiredMixin, TemplateView):
    template_name = 'secret.html'

def sampleview(request):
    return redirect('sampleview.html')   

