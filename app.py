import streamlit as st
import vectorsearch

class User:
    """
    Represents a comprehensive user profile, detailing personal, economic, family, and lifestyle
    characteristics to analyze the impact of legislative changes on the user's life.
    
    Attributes:
        name (str): Full name for personalization.
        email (str): Contact email for updates.
        date_of_birth (str): To provide age-specific advice.
        employment_status (str): Employment situation for economic impacts.
        industry (str): Sector of employment for industry-specific laws.
        education_level (str): Education level to correlate interests.
        home_ownership (str): Status of home ownership affects housing laws.
        number_of_dependents (int): Dependents for family-specific legislation.
        marital_status (str): Marital status affects certain legal statuses.
        health_status (str): General health to address healthcare laws.
        political_alignment (str): Political leanings for personalized news.
        hobbies (list): Interests that may be impacted by new laws.
        zip_code (str): For local legislation impacts.
    """
    
    def __init__(self, name: str, email: str = '', date_of_birth: str = '', employment_status: str = '',
                 industry: str = '', education_level: str = '', home_ownership: str = '', number_of_dependents: int = 0,
                 marital_status: str = '', health_status: str = '', political_alignment: str = '', hobbies: list = None, zip_code: str = ''):
        self.name = name
        self.email = email
        self.date_of_birth = date_of_birth
        self.employment_status = employment_status
        self.industry = industry
        self.education_level = education_level
        self.home_ownership = home_ownership
        self.number_of_dependents = number_of_dependents
        self.marital_status = marital_status
        self.health_status = health_status
        self.political_alignment = political_alignment
        self.hobbies = hobbies or []
        self.zip_code = zip_code

    def update_profile(self, **kwargs) -> None:
        """
        Update profile attributes based on key-value pairs provided as arguments.

        Args:
            **kwargs: Arbitrary keyword arguments corresponding to user attributes.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

def main():
    st.set_page_config(page_title="Legislative Impact Advisor", layout="wide", initial_sidebar_state="collapsed")
    
    st.title("Welcome to Your Legislative Impact Advisor")
    
    st.subheader("Meet your personal bot")
    st.write("""
        This personalized bot helps you stay informed about bills and senate activity in your area 
        that directly affects your life and finances. It simplifies the complexities of legislative impacts,
        ensuring you're well-informed and prepared for any changes.
    """)

    if 'user' not in st.session_state:
        user_name = st.text_input("Please enter your name and press [ENTER] to continue:")
        if user_name:
            st.session_state['user'] = User(name=user_name)
    else:
        user = st.session_state['user']
    # Layout: three columns (News, Chat, Preferences)
    chat_col, news_col = st.columns([1, 1])

    with news_col:
        st.subheader("Latest News")
        display_news()
    output = ""
    with chat_col:
        st.subheader("Chat Interface")
        if 'user' in st.session_state:
            output = handle_chat(st.session_state['user'])
        if len(output) > 0:
            st.text_area("Answer:", value=output, height=300)
    st.sidebar.title("User Preferences")
    if 'user' in st.session_state:
        display_preferences(st.session_state['user'])

def display_news():
    
    news = {
        'SB 532': {
            'Title': 'San Francisco Bay Area Toll Increase Act',
            'Blurb': 'This act introduces a toll rate increase for vehicles crossing state-owned toll bridges in the San Francisco Bay area, with the goal of funding transit operators facing financial shortfalls and improving transit services.',
            'Impact': 'If you frequently commute across these bridges, expect to budget an extra $1.50 per crossing from 2024 to 2028. This increase will fund public transportation, aiming to enhance the reliability and cleanliness of transit services.'
        },
        'SB 478': {
            'Title': 'Fair Advertising and Consumer Protection Act',
            'Blurb': 'The act prohibits advertising or displaying goods and services at a price that excludes mandatory fees or charges, aiming to eliminate misleading price advertisements.',
            'Impact': 'Next time you shop, the price you see will be more transparent, including all mandatory fees, which means no more surprises at checkout. This applies to goods, services, and vehicle rentals.'
        }
    }

    news['Public Transportation Fare Increase'] = {
        'Title': 'SFMTA Fare Increase Due to Extended Parking Meter Hours Block',
        'Blurb': 'Due to the Board of Supervisors blocking the implementation of extended parking meter hours, SFMTA Board is set to vote on a fare increase that could affect 90% of riders.',
        'Impact': 'If you rely on public transportation in SF, prepare for a potential 14% fare increase over the next two years. The decision is a response to budgetary constraints and aims to keep services operational and maintain quality.'
    }
    for bill_id, details in news.items():
        st.header(details['Title'])
        st.write(details['Blurb'])
        st.markdown(f"**Impact On Your Life:** {details['Impact']}")
    # To display this specific news item:

def handle_chat(user):
    input = st.text_area("Type your questions here...", height=150, key="chat_area")
    if(len(input) > 0):
        if (user):
            user_preference_str = """
            Given that my employment status is: {estatus}
            My industry is {industry},
            my education level is {edulevel}
            my home ownership status is {home}
            my nuber of dependents is {ndependents}
            my marital status is {mstatus}
            my health status is {healthstatus}
            my political alignment is {palignment}
            my hobbies is {hobbies}
            my zip code is {zipcode}

            Answer the following question (you must give me a response):

            """.format(estatus=user.employment_status, industry=user.industry, edulevel=user.education_level, home=user.home_ownership, ndependents=user.number_of_dependents, mstatus=user.marital_status, 
                    healthstatus=user.health_status, palignment=user.political_alignment, hobbies=user.hobbies, zipcode=user.zip_code)
            input = " ".join([user_preference_str, input])
            print("Query text is: " + input)
        return vectorsearch.query(input)
    return ""


def display_preferences(user: User):
    st.sidebar.info("""
        **Why set your preferences?**
        By providing your interests and concerns, our bot can tailor the information 
        and advice to your specific needs, ensuring you get the most relevant and 
        personalized experience possible.
    """)
    st.sidebar.subheader(f"{user.name}'s Preferences")

    employment_status = st.sidebar.text_input("Employment Status", user.employment_status)
    industry = st.sidebar.text_input("Industry", user.industry)
    education_level = st.sidebar.text_input("Education Level", user.education_level)
    home_ownership = st.sidebar.text_input("Home Ownership Status", user.home_ownership)
    number_of_dependents = st.sidebar.number_input("Number of Dependents", value=user.number_of_dependents, step=1)
    marital_status = st.sidebar.text_input("Marital Status", user.marital_status)
    health_status = st.sidebar.text_input("Health Status", user.health_status)
    political_alignment = st.sidebar.selectbox("Political Alignment", ['Liberal', 'Moderate', 'Conservative'], index=0)
    hobbies = st.sidebar.text_input("Hobbies (comma-separated)", ', '.join(user.hobbies))
    zip_code = st.sidebar.text_input("ZIP Code", user.zip_code)

    if st.sidebar.button("Update Preferences"):
        # Update the user's preferences
        user.update_profile(
            employment_status=employment_status,
            industry=industry,
            education_level=education_level,
            home_ownership=home_ownership,
            number_of_dependents=int(number_of_dependents),  # Convert to int as number_input returns a float
            marital_status=marital_status,
            health_status=health_status,
            political_alignment=political_alignment,
            hobbies=hobbies.split(', '),
            zip_code=zip_code
        )
        st.session_state['user'] = user
        st.sidebar.success("Your preferences have been updated!")

if __name__ == "__main__":
    main()
