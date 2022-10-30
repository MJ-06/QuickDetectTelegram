
import logging

from telegram import __version__ as TG_VER
from random_forest import *
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



def check_pattern(inp):
    inp = inp.lower()
    dis_list = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 
'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']
    pred_list=[]
    inp=inp.replace(' ','_')
    patt = f"{inp}"
    regexp = re.compile(patt)
    pred_list=[item for item in dis_list if regexp.search(item)]
    print(pred_list)
    print(inp)
    if(len(pred_list)>0):
        return 1,pred_list
    else:
        return 0,[]








First_symptom, ConfirmSymptom, Days, SymptomsList,OUTPUT = range(5)
global GlobalFSym,GlobalSym,GlobalDays,symList__
GlobalFSym,GlobalSym,GlobalDays = ['']*3
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their symptoms."""
    await update.message.reply_text(
        "Hi! My name is Doctor Bt. I will attempt to diagnose you. "
        "Send /cancel to stop talking to me.\n\n"
        "What is your first symptom",
    )

    return First_symptom


async def firstsymptom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the given symptom and asks for confirmation"""

    user = update.message.from_user
    global GlobalFSym,GlobalSym,GlobalDays,symList__
    GlobalFSym = update.message.text
    # GET SIMILAR PHRASES
    _,symList__ = check_pattern(GlobalFSym)
    # print(_,symList__)
    count = 1
    await update.message.reply_text("hmmm I think I understood what u mean."
        "Which of these phrases best describe this particular symptom ?")
    for i in symList__:
        await update.message.reply_text(str(count)+" : "+i)
        count+=1
    await update.message.reply_text(
        "Enter the digit"
    )


    return ConfirmSymptom

async def confirmsymptom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the days"""
    user = update.message.from_user
    global GlobalFSym,GlobalSym,GlobalDays,symList__
    GlobalFSym = symList__[int(update.message.text)-1]
    
    # NOTHING HERE MOVE ALONG
    await update.message.reply_text(
        "How long (in Days) have you been experiencing these symptoms ?"
    )

    return Days


async def days(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Lists similair symptoms"""
    user = update.message.from_user
    global GlobalFSym,GlobalSym,GlobalDays
    GlobalDays = update.message.text
    # FIND SIMILIAR SYMPTOMS
    GlobalSym = SimiliarSymptoms(GlobalFSym)
    count = 1
    await update.message.reply_text(
        "which of the following symptoms have u been experiencing ?"
    )
    for i in GlobalSym:
        if i==GlobalFSym:
            pass
        else:
            await update.message.reply_text(str(count)+" : "+i)
            count+=1
    await update.message.reply_text(
        "Please enter the digits separated by a space"
    )


    return SymptomsList

async def symlist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Lists similair symptoms"""
    user = update.message.from_user
    global GlobalFSym,GlobalSym,GlobalDays
    indexes = update.message.text
    simps = [GlobalFSym]
    print(GlobalSym)
    for i in indexes.split():
        simps.append(GlobalSym[int(i)])
    print(simps)
    disease = GetDisease(simps)
    print(disease)
    sever,desc,prev = DiseaseInfo(disease,simps,int(GlobalDays))
    #PREDICT DISEASE
    print(sever)
    print(desc)
    print(prev)
    #GET ALL DA DETAILS


    await update.message.reply_text(
        "You might have "+disease
    )
    await update.message.reply_text(
        sever
    )
    await update.message.reply_text(
        desc
    )
    await update.message.reply_text(
        'Some precautions that you can take are:'
    )
    count = 0
    for i in prev:
        await update.message.reply_text(
        str(count)+': '+i
        )
        count+=1
    return ConversationHandler.END



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END




def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5766496564:AAHgQqisUeYaGRkpjT_KM-ulCJH-QdSla9Q").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            First_symptom: [MessageHandler(filters.TEXT & ~filters.COMMAND, firstsymptom)],
            ConfirmSymptom: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmsymptom)],
            Days: [MessageHandler(filters.TEXT & ~filters.COMMAND, days)],
            SymptomsList: [MessageHandler(filters.TEXT & ~filters.COMMAND, symlist)],



        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()