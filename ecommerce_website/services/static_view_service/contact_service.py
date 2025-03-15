class ContactService:

    @staticmethod
    def get_contact_data(store_data):
        socials_html = ""
        for platform, link in store_data['socials'].items():
            if platform == "facebook":
                socials_html += f"""
                    <a href="{link}" class="text-gray-400 hover:text-gray-300" target="_blank">
                        <span class="sr-only">Facebook</span>
                        <svg class="size-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                            <path fill-rule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clip-rule="evenodd" />
                        </svg>
                    </a>
                """
            elif platform == "instagram":
                socials_html += f"""
                    <a href="{link}" class="text-gray-400 hover:text-gray-300" target="_blank">
                        <span class="sr-only">Instagram</span>
                        <svg class="size-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                            <path fill-rule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clip-rule="evenodd" />
                        </svg>
                    </a>
                """
        return {

            "data": [
                {
                    "title": "Contact opnemen",
                    "text": f"Mocht u ergens niet uitkomen of is er iets niet duidelijk genoeg,<br>"
                    f"dan kunt u contact met ons opnemen via het emailadres <a class='text-orange-500 font-medium' href='mailto:{
                        store_data['contact_email']}'>"
                    f"{store_data['contact_email']}</a>. "
                    f"Wij zijn beschikbaar voor vragen op werkdagen tussen <strong>{
                        store_data['opening_time_week']}</strong>.<br><br>"
                    f"Soms kan het zijn dat uw vraag overleg nodig heeft en onze reactie hierdoor wat langer kan duren.<br>"
                    f"In dit geval zullen wij dit ten alle tijden met u communiceren.<br><br>"
                    f"Wij streven ernaar om binnen maximaal <strong>2 werkdagen</strong> u met een antwoord te hebben voorzien."
                },
                {
                    "title": "Veelgestelde vragen",
                    "text": "Soms kan het zijn dat je een vraag hebt die wij al meerdere keren hebben beantwoord en het antwoord hiervan al bekend is.<br><br>"
                    "In elk geval is het altijd handig om onze <a href=\"#faq\" class=\"text-orange-500 font-medium\">Veelgestelde vragen</a> te raadplegen. Misschien staat uw antwoord hier al bij.<br><br>"
                    "En mocht het zo zijn dat u alsnog vragen heeft, dan zullen wij altijd ruimte maken om je hier zo goed mogelijk bij te helpen."
                },

                {
                    "title": "Sociale media",
                    "text": "Uiteraard zijn wij ook bereikbaar via sociale media.<br>"
                    "Het is onze bedoeling om onze klanten zo veel mogelijk updates te geven over onze <a href=\"/products\" class=\"text-orange-500 font-medium\">producten</a> en actuele <a href=\"/discounts\" class=\"text-orange-500 font-medium\">aanbiedingen</a>.<br><br>"
                    "Daarnaast is het gewoon toegestaan om productgerelateerde vragen te stellen, hier proberen wij zo snel mogelijk op te reageren.<br><br>"
                    "Neem gerust een kijkje bij onze <strong>socials</strong>!",
                    "additional_data": socials_html,

                }
            ],
            "extra": "Kom je ergens niet uit?",
            "name": "Klantenservice",
            "header": "Wij regelen het voor u!",
            "description": "Bij onze klantenservice streven we ernaar om u de best mogelijke service te bieden.<br><br>"
            "Wij doen ons uiterste best om uw bestelling snel en probleemloos bij u af te leveren. Omdat een vlotte en betrouwbare <a class='font-medium text-orange-500' href='/payment-return-service#delivery'>levering</a> voor ons net zo belangrijk is als voor u, werken we nauw samen met onze leveranciers en fabrikanten om uw bestelling zo snel mogelijk in goede staat te bezorgen.<br><br>"
            "Hoewel we alles in het werk stellen om een tijdige levering te garanderen, kunnen levertijden variëren door factoren buiten onze controle. Mocht er onverhoopt vertraging optreden, dan informeren we u zo snel mogelijk en zoeken we samen naar een passende <strong>oplossing</strong>."

        }
