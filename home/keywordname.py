from flashtext.keyword import KeywordProcessor
import re
import nltk
# nltk.download('punkt')
from .models import women
from nltk.corpus import stopwords
# nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from django.apps import apps
# nltk.download('wordnet') 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet 

def predictCrimeName(desc,tableName): 
    model_you_want = apps.get_model(app_label='home', model_name=tableName)
    wnl = WordNetLemmatizer() 
    all_stopwords = stopwords.words('english')
    
    
    sw_list = ['etc',',','.','girl','girls']
    all_stopwords.extend(sw_list)
    crimeName_list = []
    text_tokens = word_tokenize(desc)

    tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
    filtered_sentence = (" ").join(tokens_without_sw)
    
    # keyword_dict = {}
    # print(all_stopwords)
    # for e in model_you_want.objects.all():
    #     crimeName_list.append(e.crimeName)
    # for e in model_you_want.objects.all():
    #     text_tokens = word_tokenize(e.crimeName)
    #     tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
    #     synonyms = []
    #     for words in tokens_without_sw: 
             
    #         for syn in wordnet.synsets(words): 
    #             for l in syn.lemmas(): 
    #                 synonyms.append(l.name()) 
    #     # print((synonyms))
    #     keyword_dict[e.crimeName] = synonyms
        
    
    
            # print(words + " ---> " + wnl.lemmatize(words)) 
    keyword_processor = KeywordProcessor(case_sensitive = False)
    keyword_dict = {
    'Rape':['rape','raped'],
#     'Gang Rape':['gang rape','pack', 'ring', 'mob', 'crowd', 'crew', 'gang', 'bunch',   'work_party', 'people' , 'gang_up'],
    'Punishment for causing death or resulting in persistent vegetative state of victim':['murder','death','persistent','coma','died','Dead', ' Die' , 'Died','kill','murdered'],
    'Dowry Deaths': ['dowry death', 'dowery', 'dower', 'dahej','death', 'decease', 'expiry',  'dying', 'demise',  'last', 'Death', 'end', 'destruction'],
    'Stalking': ['stalk', 'stalking', 'follow','monitor','internet','email','social media'],
    'Sexual Harassment':['sexual', 'intimate',  'harassment', 'harassing','torment',  'molestation','Unwelcome', 'touching','bad touch','Showing pornographic'],
    'Theft': ['steal', 'grab','snatch','snatching'],
#     'kidnap': ['kidnapping','kidnapped','kidnap'],
#     'Murder':['kill','death','homicide','maar diya','jaan se maar diya','murder','died','Dead', ' Die' , 'Died'],
    'Cruelty by Husband and Relatives': ['cruelty', 'inhuman_treatment', 'cruelty', 'mercilessness', 'pitilessness', 'ruthlessness', 'cruelty', 'cruelness', 'harshness', 
    'husband', 'hubby', 'married_man', 'conserve', 'husband', 'economize', 'economise', 'relative', 'relation', 'relative', 'congener', 
    'congenator', 'congeneric'],
    'Importation of girl from foreign country': ['importing', 'importation', 'import', 'foreign', 'strange', 'state', 'nation', 'country', 'land', 'area', ],
    'Attempt  to throw acid': ['attempt', 'effort', 'endeavor', 'endeavour', 'try', 'attack', 'attempt',  'seek', 'attempt', 'essay', 'assay', 'undertake', 'set_about', 'attempt',  'stroke',   'shed', 'cast', 'cast_off', 'shake_off', 'throw_off', 'throw_away', 'throw', 'flip', 'switch', 'project', 'cast',  'discombobulate', 'throw', 'hurl',  'hold',   'make', 'give', 'throw', 
            'throw',   'discombobulate', 'acid',  'back_breaker', 'battery-acid',  'sulfurous', 'sulphurous', 
            'virulent', 'vitriolic', 'acidic', 'acid', 'acidulent', 'acidulous', 'acid'],
    'Kidnapping, abducting or inducing woman to compel her marriage, etc': ['kidnapping', 'kidnap', 
    'nobble', 'abduct', 'nobble', 'abduct', 'abducent', 'abducting', 'inducement', 'inducing', 'induce', 'bring_on',  'stimulate', 'cause',  'stimulate', 'rush', 'hasten','induct','compel', 'oblige', 'obligate',  'marriage', 'matrimony', 'union', 'spousal_relationship', 'wedlock', 'married_couple', 'man_and_wife',  'wedding', 'marriage_ceremony']
    
    }

    keyword_processor.add_keywords_from_dict(keyword_dict)
    crimeName = keyword_processor.extract_keywords(filtered_sentence)
     # intilize a null list
    uniqueCrimeList = []
     
    # traverse for all elements
    for x in crimeName:
        # check if exists in unique_list or not
        if x not in uniqueCrimeList:
            uniqueCrimeList.append(x)
    return uniqueCrimeList