import os
from datetime import datetime
import json

def get_newest_outland_journal_file(folder_path):
    try:
        text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        if not text_files:
            print(f"No .txt files found in {folder_path}")
            return None
        
        newest_file = max(text_files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
        return os.path.join(folder_path, newest_file)
    except FileNotFoundError:
        print(f"Error: The folder '{folder_path}' does not exist.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to access '{folder_path}'.")
        return None
    except Exception as e:
        print(f"Error accessing folder '{folder_path}': {e}")
        return None
    
def process_Items_data(file_path):
    data = {
    "name": None,
    "items": []
}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip()
                if "System: Welcome" in line:
                    name = line.split("System: Welcome")[1].strip()
                    data["name"] = name
                    
                if "[Razor]: ID:" in line:
                    item_data = line.split("[Razor]: ID:")[1].strip()
                    parts = item_data.split()
                    
                    if len(parts) >= 2:
                        item_id = parts[0]
                        remaining = parts[1:]
                        
                        if remaining[-1].isdigit():
                            amount = int(remaining[-1])
                            description = " ".join(remaining[:-1])
                        else:
                            amount = 1
                            description = " ".join(remaining)
                            
                        description = description.rstrip(':')
                            
                        item = {
                            "id": item_id,
                            "description": description,
                            "amount": amount
                        }
                        data["items"].append(item)
                
                elif "System: You deposit" in line:
                    parts = line.split("System: You deposit")
                    if len(parts) > 1:
                        deposit_data = parts[1].strip()
                        amount_str = deposit_data.split(" gold")[0].replace(",", "").strip()
                        if amount_str.isdigit():
                            amount = int(amount_str)
                            item = {
                                "id": "9999999999",
                                "description": "gold",
                                "amount": amount
                            }
                            data["items"].append(item)

        return data
    
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied to read '{file_path}'.")
        return []
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")
        return []

def merge_identical_items(data):

    merged_items = {}
    
    # Extract items from the data dictionary
    items = data["items"]
    
    for item in items:
        desc = item["description"]
        if desc in merged_items:
            merged_items[desc]["amount"] += item["amount"]
        else:
            merged_items[desc] = {
                "id": item["id"],
                "description": desc,
                "amount": item["amount"]
            }
    
    # Return a new dictionary with the original name and merged items
    return {
        "name": data["name"],
        "items": list(merged_items.values())
    }

def save_Items_json(vendors, output_dir, input_file_name):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H") 
        output_file = os.path.join(output_dir, f"{input_file_name}_Items_{timestamp}.json")

        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(vendors, json_file, indent=4, ensure_ascii=False)

        print(f"JSON Data saved to: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error saving JSON data: {e}")
        return None
    
def display_inventory_data(items, merged_items,name):
    print(f"Name: {name}")
    print("\n====================== Inventory Summary ======================")
    print(f"Found {len(items)} total items, merged into {len(merged_items)} unique items.\n")
    for item in merged_items:
        print(f"(ID: {item['id']})  {item['description']}, Amount: {item['amount']}")
        
    print("\n===============================================================")

def save_Items_data(items, merged_items, output_dir, input_file_name, name):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H")
        output_file = os.path.join(output_dir, f"{input_file_name}_Items_{timestamp}.txt")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Processed Data from {input_file_name}\n")
            f.write(f"Name: {name}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("====================== Inventory Summary ======================\n")
            f.write(f"Found {len(items)} total items, merged into {len(merged_items)} unique items.\n\n")
            for item in merged_items:
                f.write(f"(ID: {item['id']})  {item['description']}, Amount: {item['amount']}\n")
        
            f.write("\n===============================================================")
            
        print(f"Data saved to: {output_file}")
        return output_file
    except PermissionError:
        print(f"Error: Permission denied to write to '{output_dir}'.")
        return None
    except Exception as e:
        print(f"Error saving data to '{output_dir}': {e}")
        return None      

def main():
    input_folder_path = r"C:\Program Files (x86)\Ultima Online Outlands\ClassicUO\Data\Client\JournalLogs"
    output_directory = os.path.join(r"C:\Users\dcorr\Documents", "Processed")
    
    if not os.path.exists(input_folder_path):
        print(f"Error: Input folder '{input_folder_path}' does not exist. Please check the path.")
        return

    newest_file = get_newest_outland_journal_file(input_folder_path)
    if not newest_file:
        print("No further processing due to missing files or access issues.")
        return

    print(f"Processing file: {newest_file}")
    base_name = os.path.splitext(os.path.basename(newest_file))[0]
    
    # Get the full data structure
    data = process_Items_data(newest_file)
    if not data or not data["items"]:
        print("Processing failed or no items found. Check error messages above.")
        return
    
    # Merge items using the full data structure
    merged_data = merge_identical_items(data)
    name = data["name"]
    # Extract items for display and text saving
    items = data["items"]  # Original unmerged items
    merged_items = merged_data["items"]  # Merged items
    
    display_inventory_data(items, merged_items,name)
    
    # Save full JSON data (unmerged)
    save_Items_json(data, output_directory, base_name)
    
    # Save text file with merged items and name
    save_Items_data(items, merged_items, output_directory, base_name, name)

if __name__ == "__main__":
    main()
    
    
    
# Copy this part at the beginning of your loot organiser
# TODO : change list of items to search for curent list is for vendor items
#  
#           if Itemindexer = 1 and find jootbag backpack as container
#                while findtype 576|1489|1496|1763|2207|2213|2219|2323|2409|2413|2418|2419|2425|2463|2475|2594|2595|2596|2597|2726|2807|2845|3091|3092|3108|3203|3204|3206|3207|3211|3214|3215|3217|3219|3220|3221|3222|3223|3224|3225|3226|3227|3228|3229|3230|3231|3232|3233|3234|3235|3237|3238|3239|3240|3241|3242|3243|3255|3256|3257|3258|3259|3262|3263|3268|3271|3272|3273|3288|3302|3305|3306|3307|3308|3309|3310|3311|3312|3313|3314|3320|3323|3326|3329|3332|3340|3341|3342|3343|3344|3345|3346|3347|3348|3365|3366|3367|3368|3370|3372|3374|3376|3377|3381|3383|3391|3392|3492|3496|3519|3520|3527|3528|3529|3530|3531|3568|3569|3591|3637|3638|3639|3640|3641|3642|3648|3649|3650|3651|3656|3657|3658|3659|3699|3700|3708|3709|3712|3713|3714|3715|3717|3718|3719|3720|3721|3722|3735|3736|3737|3738|3740|3741|3742|3762|3763|3764|3773|3786|3787|3788|3789|3790|3791|3792|3793|3794|3827|3828|3829|3830|3831|3832|3833|3834|3835|3836|3837|3838|3839|3840|3841|3842|3843|3844|3856|3859|3861|3862|3865|3873|3877|3878|3885|3892|3897|3898|3907|3908|3909|3910|3911|3912|3913|3914|3915|3916|3917|3918|3919|3920|3921|3922|3932|3933|3934|3935|3936|3937|3938|3939|3985|3999|4025|4026|4201|4225|4226|4248|4249|4250|4251|4252|4253|4254|4255|4256|4257|4258|4259|4277|4656|4831|5039|5040|5041|5042|5043|5044|5045|5046|5049|5050|5056|5059|5060|5061|5063|5070|5074|5075|5076|5078|5085|5089|5090|5101|5103|5105|5106|5112|5113|5114|5115|5116|5117|5118|5119|5120|5121|5122|5123|5124|5125|5126|5127|5129|5131|5132|5135|5138|5139|5142|5143|5144|5146|5176|5177|5178|5179|5180|5181|5182|5183|5184|5185|5186|5187|5188|5189|5190|5191|5201|5203|5204|5205|5207|5355|5356|5359|5360|5361|5362|5363|5364|5365|5366|5370|5373|5374|5376|5377|5378|5379|5416|5418|5421|5453|5534|5645|5661|5662|5899|5900|5901|5902|5903|5904|5905|5906|5981|5982|5983|5984|5985|5986|5987|5988|6039|6049|6187|6193|6238|6464|7026|7027|7029|7031|7033|7034|7035|7107|7109|7116|7127|7128|7129|7130|7131|7132|7139|7140|7141|7142|7143|7144|7145|7146|7147|7148|7149|7150|7151|7152|7153|7154|7155|7156|7157|7158|7159|7160|7161|7162|7169|7170|7173|7175|7177|7179|7181|7369|7370|7371|7372|7377|7377|7378|7379|7380|7381|7382|7383|7384|7385|7610|7732|7866|7947|8012|8031|8032|8040|8041|8042|8043|8044|8417|8438|8454|8455|8478|8479|8480|8481|8484|8501|8502|8503|8750|8751|8752|8753|8786|8787|8826|8901|9002|9006|9010|9076|9078|9079|9253|9917|10136|10245|10247|10324|10527|10827|11225|11227|11229|11231|11552|11761|11762|11763|11764|11881|11882|11883|11884|11885|11886|11887|11888|11889|11890|11891|11893|11895|11897|11942|12215|12282|12320|12321|12322|12323|12324|12686|13278|13290|13291|13292|13297|13298|13299|13300|13301|13305|13307|13308|13309|13310|13311|13312|13313|13314|13316|13318|13319|13320|13321|13328|13330|13335|13336|13591|13597|13613|14428|14442|14444|14448|14450|14451|14454|14456|14458|14470|14484|14490|14496|14506|14512|14514|14520|14522|14530|14536|14538|14542|14544|14562|14568|14571|14574|14594|15178|15293|15294|15295|15296|15297|15298|15505|15506|15507|15508|15509|15511|15514|15516|15518|15519|15520|15521|15522|15523|15524|15577|15580|15635|15638|16898|17081|17083|17087|17686|18075|18082|18083|18085|18087|18218|18233|18282|18283|18400|18652|18653|18658|18704|19199|19226|19227|19228|19229|19230|19231|19232|19233|19234|19235|19236|19237|19238|19239|19240|19241|19242|19243|19244|19245|19246|19247|19248|19249|19250|19251|19252|19253|19254|19255|19256|19370|19372|19403|19508|19512|19513|19520|19521|19522|19524|19525|19528|19529|19532|19582|19583|19785|19793|19795|19799|19805|19812|19814|19821|19822|20006|20008|20010|20012|20014|20016|20309|20374|20375|20376|20377|20378|20379|20381|20383|20384|20385|20391|20392|20466|20467|20495|20496|20499|20502|21387|21397|21398|21399|21400|21401|21402|21403|21404|21405|21780|21781|21783|21784|21785|21786|21787|21788|21789|21790|21791|21797|21798|21799|21800|21801|21803|21804|21805|21806|21807|21808|21809|21810|21814|21818|21824|21826|21827|21828|21829|21830|21831|21835|21836|21838|21840|21841|21842|21843|21844|21845|21847|21848|21849|21852|21853|21856|21859|21860|21861|21862|21863|21864|21865|21866|21867|21868|21870|21871|21872|21873|21874|21875|21876|21877|21878|21879|21880|21881|21882|21883|21884|21885|21886|21889|21891|21893|21894|21895|21896|21897|21898|21899|21901|21902|21904|21905|21906|21907|21908|21909|21911|21917|21918|21921|21923|21924|21925|21926|21927|21929|21931|21933|21934|21935|21936|21937|21938|21939|21940|21942|21943|21944|21945|21947|21948|21949|21950|21951|21953|21954|21956|21957|21960|21962|21963|21964|21969|21978|21981|21988|21996|21997|21998|21999|22151|22152|22153|22154|22155|22157|22158|22163|22164|22165|22166|22167|22168|22169|22170|22171|22172|22173|22174|22175|22177|22178|22179|22180|22181|22182|22183|22184|22185|22186|22187|22188|22189|22190|22191|22192|22193|22194|22195|22196|22197|22199|22261|22264|22272|22285|22286|22287|22288|22289|22290|22291|22292|22293|22294|22295|22296|22297|22298|22326|22336|22417|22418|22419|22420|22421|22422|22423|22426|22427|22428|22429|22430|22431|22432|22433|22434|22435|22436|22437|22438|22439|22440|22441|22442|22443|22444|22445|22449|22451|22453|22455|22456|22457|22458|22459|22460|22461|22462|22465|22468|22469|22471|22472|22473|22475|22476|22477|22489|22717|22845|22873|23009|23034|23035|23048|23049|23050|23051|23052|23774|23867|23868|23869|23870|23871|23872|23873|23874|23875|23876|23877|23878|23879|23880|23881|23882|23883|23884|23885|23886|23887|23889|23890|23891|23892|23893|23894|23895|23899|23900|23901|23902|23903|23904|23905|23906|23907|23908|23909|23910|23953|23954|23955|23956|23996|23997|24175|24178|24179|24181|24182|24183|24184|24187|24188|24190|24191|24193|24195|24196|24197|24199|24208|24246|24345|24382|24383|24384|24385|24386|24387|24388|24389|24390|24391|24392|24393|24394|24395|24396|24397|24398|24399|24400|24401|24402|24403|24404|24405|24406|24407|24408|24409|24410|24411|24412|24413|24414|24415|24416|24417|24418|24419|24420|24421|24422|24423|24424|24425|24426|24427|24428|24429|24430|24431|24432|24433|24434|25359|25490|25526|25527|25529|25531|25533|25535|25538|25569|25581|25583|25647|25670|25730|25750|25758|25759|26640|26664|26669|26670|26671|26672|26688|26689|26693|26700|26701|26719|26720|26721|26724|26732|26734|26735|26736|26737|27561|27562|27563|27564|27565|27577|27580|27584|27611|27612|27640|27642|27666|27668|28237|28238|28263|28314|28322|28341|28344|28350|28376|28410|28760|28765|28768|28775|28795|28799|28803|28879|28880|28881|28883|28885|28888|28908|28909|28910|28911|28924|28993|28994|28995|29001|29012|29024|29025|29026|29027|29028|29029|29030|29031|29032|29033|29034|29035|29036|29037|29038|29040|29045|29064|29103|29104|29105|29106|29107|29108|29142|29343|29345|29350|29352|29354|29355|29382|29421|29425|29428|29430|29431|29463|29495|29497|29498|29502|29773|29774|29832|29833|29868|30561|30562|30563|30564|30565|30566|30567|30568|30573|30574|30575|30576|30577|30578|30579|30580|30582|30583|30585|30586|30587|30588|30589|30590|30591|30592|30596|30599|30601|30602|30603|30604|30608|30609|30610|30611|30612|30613|30614|30615|30617|30618|30621|30622|30623|30624|30625|30626|30627|30628|30629|30630|30631|30632|30633|30634|30635|30636|30637|30638|30639|30640|30641|30642|30643|30644|30645|30646|30647|30648|30649|30650|30651|30652|30653|30655|30657|30658|30659|30660|30661|30662|30663|30765|30766|30767|30768|30769|30770|30771|30772|30773|30775|30776|30778|30818|30819|30821|30822|30823|30825|30826|30827|30828|30829|30850|30851|30852|30853|30854|30855|30856|30857|30858|30859|30860|30866|30867|30868|30869|30870|30871|30872|30878|30967|30969|30970|30971|30972|30973|30974|30975|30976|30977|30978|30979|30980|30981|30982|30983|30984|30985|30986|30988|30989|30990|30991|30992|30993|30994|30995|30996|30997|30998|30999|31000|31001|31002|31003|31004|31005|31006|31007|31008|31009|31010|31011|31012|31014|31015|31017|31019|31021|31023|31025|31027|31029|31031|31033|31035|31037|31038|31041|31043|31045|31047|31049|31051|31053|31055|31117|31118|31119|31120|31121|31122|31123|31124|31125|31126|31128|31130|31141|31142|31143|31144|31148|31149|31150|31151|31152|31153|31154|31155|31156|31157|31163|31164|31166|31169|31172|31176|31178|31180|31182|31184|31186|31188|31190|31191|31197|31198|31199|31200|31201|31202|31203|31204|31206|31207|31210|31211|31212|31213|31214|31215|31216|31231|31232|31233|31234|31236|31237|31238|31239|31243|31244|31245|31246|31247|31248|31249|31250|33323|33342|33343|33344|33345|36752|37049|37050|37051|37052|37053|37054|37055|37056|37057|37060|37061|37063|37064|37065|37066|37067|37068|37181|39158|39163|39264|39343|39344|39345|39346|39347|39348|39349|39350|39351|39352|39353|39517|39889|39891|39892|39896|39897|39898|39905|39909|39911|39912|39916|39917|39918|40697|40698|40701|40702|40800|40954|40955|40958|40959|40960|40980|40981|41449|41451|41453|41455|41459|41460|41461|41462|41466|41509|41510|41584|41596|41605|41607|41614|41619|41631|41632|41634|41638|41642|41646|41650|41662|41669|41671|41674|41675|41679|41680|41967|41973|41998|42000|42003|42227|42239|42240|42242|42243|42244|42380|42493|42516|42517|42519|42564|42574|42648|42665|42830|42832|42834|42836|42843|42847|42850|42851|42854|43159|43160|43161|43162|43163|43164|43165|43166|43167|43168|43169|43170|43171|43172|43173|43174|43175|43176|43177|43178|43179|43180|43181|43182|43206|43207|43208|43209|43210|43277|43279|43320|43375|43453|43461|44127|44129|44131|44310|44312|44314|44315|44328|44716|44718|44720|44722|44724|44795|44796|44797|44798|44799|44800|44801|44804|44805|44808|44810|44836|44837|44846|44919|44921|44923|44925|44926|44929|44949|44951|44953|44955|44957|44959|44986|44987|44997|44998|45002|45120|45156|45157|45182|45193|45208|45211|45214|45216|45218|45220|45222|45235|45236|45238|45239|45241|45242|45246|45247|45248|45250|45251|45252|45254|45255|45257|45281|45282|45285|45300|45315|45316|45320|45371|45372|45373|45374|45375|45376|45377|45378|45379|45380|45381|45382|45383|45384|45385|45386|45387|45388|45389|45390|45391|45392|45393|45394|45395|45396|45397|45398|45399|45400|45401|45402|45403|45404|45405|45406|45407|45408|45409|45410|45411|45412|45413|45414|45415|45416|45417|45418|45419|45420|45421|45422|45423|45424|45425|45426|45427|45428|45429|45430|45828|45830|45832|45835|45839|46527|47107|47109|47111|47148|47194|47201|47203|47205|47207|47209|47211|47213|47214|47217|47219|47221|47223|47225|47227|47229|47564|47565|47566|47567|47568|47569|47570|47571|47572|47573|47574|47575|47576|47577|47578|47578|47580|47581|47582|47583|47584|47585|47586|47587|47588|47589|47590|47591|47592|47593|47594|47595|47596|47597|47598|47599|47600|47601|47602|47603|47604|47605|47606|47607|47608|47609|47610|47611|47612|47613|47614|47615|47616|47617|47618|47619|47620|47621|48261|48291|48295|48299|48302|48303|48357|48358|48359|48360|48361|48362|48363|48364|48365|48366|48367|48368|48369|48370|48371|48372|48373|48374|48375|48376|48377|48378|48379|48380|48381|48382|48383|48384|48385|48386|48387|48388|48389|48390|48391|48392|48393|48394|48395|48396|48397|48398|48399|48400|48401|48402|48403|48404|48405|48406|48407|48793|48802|48805|48807|48815|48820|48822|48823|48825|48827|49035|49039|49042|49053|49058|49063|49070|49079|49088|49100|49110|49113|49114|49118|49211|49215|49224|49229|49235|49236|49291|49293|49295|49297|49299|49301|49302|49306|49314|49316|49324|49330|49334|49359|49382|49527|49535|49554|49555|49557|49561|49571|49574|49578|49580|49582|49584|49597|49613|49633|49650|49672|49683|49698|49738|49749|49760|49762|49763|49764|49765|49766|49767|49768|49769|49770|49784|49789|49804|49806|49807|49810|49812|49814|49816|49819|49857|49985|50285|50298|50308|50632|50651|50675|51016|51037|51041|51043|51045|51047|51049|51055|51056|51058|51060|51062|51064|51076|51078|51094|51098|51100|51200|51201|51202|51203|51204|51205|51206|51207|51208|51209|51210|51211|51212|51213|51214|51215|51216|51217|51218|51219|51220|51221|51222|51223|51224|51225|51226|51227|51228|51229|51230|51231|51232|51233|51234|51235|51236|51237|51238|51239|51240|51241|51242|51243|51244|51245|51246|51247|51248|51249|51250|51251|51252|51253|51254|51255|51256|51257|51258|51259|51260|51261|51262|51263|51264|51265|51266|51267|51268|51269|51270|51271|51272|51273|51274|51275|51276|51277|51278|51279|51280|51281|51282|51283|51284|51285|51286|51287|51288|51289|51290|51291|51292|51293|51294|51295|51296|51297|51298|51299|51300|51301|51302|51303|51304|51305|51306|51307|51308|51309|51310|51311|51312|51313|51314|51315|51316|51317|51318|51319|51320|51321|51322|51323|51324|51325|51326|51327|51328|51329|51330|51331|51332|51333|51334|51335|51336|51337|51338|51339|51340|51341|51342|51343|51344|51345|51346|51347|51348|51349|51350|51351|51352|51353|51354|51355|51356|51357|51358|51359|51360|51361|51362|51363|51364|51365|51366|51367|51368|51369|51370|51371|51372|51373|51374|51375|51400|51401|51402|51403|51404|51405|51406|51407|51408|51409|51410|51411|51412|51413|51414|51415|51416|51417|51418|51419|51420|51421|51422|51423|51424|51425|51426|51427|51428|51429|51430|51431|51432|51433|51434|51435|51436|51437|51438|51439|51440|51441|51442|51443|51444|51445|51446|51447|51448|51449|51450|51451|51452|51453|51454|51455|51456|51457|51458|51459|51460|51461|51462|51463|51464|51465|51466|51467|51468|51469|51470|51471|51472|51473|51474|51475|51476|51477|51478|51479|51494|51965|51986|51988|51996|51998|52000|52002|52030|52032|52034|52044|52060|52140|52142|52144|52146|52149|52200|52203|52216|52217|52219|52221|52227|52229|52231|52233|52236|52276|52414|52417|52486|52488|52496|52504|52506|52507|52512|52514|52577|52618|52620|52622|52630|52634|52648|52649|52651|52652|52653|52655|52675|52676|52677|52678|52679|52689|52696|52703|52705|52731|52757|52817|52819|52821|52824|52831|52844|52867|52870|52932|52957|52960|53037|53038|53053|53127|53134|53139|53161|53178|53179|53181|53192|53326|53327|53331|53334|53338|53343|53347|53355|53375|53408|53409|53411|53413|53415|53416|53418|53422|53441|53450|53451|53547|53548|53549|53550|53551|53552|53553|53554|53555|53556|53557|53558|53559|53560|53561|53562|53563|53564|53565|53566|53567|53568|53569|53570|53571|53572|53573|53574|53575|53576|53577|53578|53579|53580|53581|53582|53583|53584|53585|53586|53587|53588|53589|53590|53591|53592|53593|53594|53595|53596|53597|53598|53599|53600|53601|53602|53603|53604|53605|53606|53607|53608|53609|53610|53611|53675|53681|53769|53775|53792|53813|53821|53837|53869|53877|53892|53895|53899|53902|53904|53906|53912|53920|53946|53954|53963|53964|53969|53982|54088|54099|54103|54107|54109|54111|54115|54121|54161|54162|54163|54164|54167|54182|54184|54185|54191|54192|54194|54195|54197|54199|54201|54205|54207|54214|54216|54218|54220|54221|54222|54319|54321|54327|54357|54359|54361|54366|54454|54455|54459|54463|54474|54476|54486|54488|54490|54496|54497|54498|54557|54563|54572|54574|54576|54578|54580|54582|54583|54584|54590|54600|54608|54627|54630|54639|54650|54652|54656|54659|54664|54666|54678|54682|54684|54717|54718|54752|54753|54754|54785|54789|54793|54815|54832|54844|54847|54854|54856|54856|54859|54864|54869|54883|54887|54901|54908|54917|54920|54923|54925|54947|54951|54953|54965|54973|54981|54984|54997|55003|55005|55013|55041|55047|55052|55108|55121|55139|55157|55159|55161|55164|55173|55193|55207|55209|55211|55217|55225|55234|55239|55247|55318|55336|55338|55340|55376|55386|55398|55400|55402|55409|55419|55432|55434|55443|55447|55450|55456|55457|55543|55547|55555|55578|55590|55607|55668|55674|55675|55694|55696|55736|55738|55741|55743|55744|55745|55747|55751|55753|55755|55763|55764|55765|55773|55775|55777|55785|55787|55789|55791|55793|55818|55820|55822|55824|55842|55843|55845|55849|55855|55859|55863|55867|55869|55874|55879|55887|55890|55926|55933|55939|55963|56144|56160|56162|56164|56170|56173|56176|56181|56186|56192|56204|56206|56212|56214|56215|56235|56238|56250|56252|56274|56275|56276|56293|56308|56311|56313|56314|56319|56323|56326|56330|56381|56387|56390|56392|56393|56395|56399|56401|56409|56418|56424|56426|56433|56436|56445|56453|56633|56663|56665|56671|56678|56680|56682|56684|56686|56688|57710|57705|57697|57618|57567|57659|57597|57652|57626|57583|57636|57644|57620|57560|57674|57563|57612|57610|11898|31262|11849|11850|11851|11853|11855|11856|11858|11859|11857|11641|58135|57832|11478|57938|25174|58137|25107|57937|25110|57939|25508|57943|58133|57866|15808|25161|57941|58131|58058|57918|57822|58149|45285|49749|46527|55247|49738|31259|31253|31254|31257|31252|31258|31256|31255|31263|37477|7117|54948|11896|18044|18045|18046|18047|18048|18049 container as foundItem
#                getlabel 'foundItem' desc
#                    sysmsg "ID: {{foundItem}} {{desc}}" 23
#                    @ignore foundItem
#                        if insysmsg "The world will save in"
#                        while not insysmsg "World save complete."
#                        pause 1000
#                        endwhile
#                        endif 
#                endwhile
#           endif