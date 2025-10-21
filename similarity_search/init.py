 
from langchain_community.vectorstores import Chroma

preloaded_responses_collection=Chroma(persist_directory="./chroma_db",embedding_function=embedding_fun)
   
preloaded_responses_collection.add_texts(texts=[
    "To consume food from the home tab: you need to swipe food stubs left or right",
    "To check food info or edit its macros: you need to click on the info icon on top of the food stub",
    "To delete food from food list: you need to click the red trashbin on the top left corner of the food stub",
    "To access each macro progress: you need to click on the specific macro (protein/carbs/calories) bar",
    "To multiple eating portions: you need to use the up and down buttons on the far right of food stub",
    "To quick check food macros: you need to click on the food stub",
    "To quick uncheck food macros: you need to click on the food stub again",
    "To sort food list accordingly: you need to click on the floating button on the right of the food list",
    "To refresh your food in case of an error or update failure: you need to click on the small reload button under the macros dashboard on the home tab",
    "To refresh your consumed food list in case of an error or update failure: you need to click on the small reload button or pull the list down under days listing inside consumed tab",
    "To check up to past 7 days progress: you need to click on the previous day date on the list of days above on the home tab",
    "To edit macro goals or reset today's progress manually: you need to click on the pen on the top left of home tab",
    "To search for foods by name: you need to use the search bar",
    "To remove popping notifications: you need to click on the dismiss button on the notification",
    "To add food on the go instantly: you need to proceed to home tab and use the center tab camera popping up",
    "To check up past 7 days consumed food: you need to proceed to consumed tab and use the dates buttons to access the exact date",
    "To add daily consumable food: you need to access add tab and either add manually or just use the camera icon and let our nutritionist AI do the work",
    "To change portion from g/ml to kg/L: you need to click on the g/ml button; it will go back and forth for change",
    "To set your goals automatically based on your anthropometric/physical measurements: you need to access goals tab and fill out 3 sub-tabs (calories -> protein -> carbs) in order",
    "To check your analytics: you need to access analytics tab",
    "To check your profile: you need to access profile tab",
    "To change your anthropometric/physical measurements (weight/height/age): you need to access profile tab settings",
    "To read our Terms & Conditions: you need to access them from the profile tab",
    "To reach out to our FAQ bot support: you need to access the floating bubble on the profile tab",
    "To reach our 24/7 support team and for more questions: you need to send an email to our team in the profile settings",
    "To logout: you need to click on the logout button on the top right of profile tab",
    "To login/create an account: you need to access login or create new account buttons after launching app and after being logged out",
    "To access our premium service: you need to wait for the lazy developer to add premium features (it's disabled for now)",
    "To consume your food daily: you need to wait till midnight according to your timezone on your device (it will be reset automatically)"
])