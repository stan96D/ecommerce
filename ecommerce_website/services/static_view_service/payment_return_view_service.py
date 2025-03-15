class PaymentReturnViewService:

    @staticmethod
    def get_payment_return_data(payment_methods):

        payments_html = ""
        for payment_method in payment_methods:
            payments_html += f"""
                <div class="payment-method">
                    <img src="{payment_method.image_url}" alt="{payment_method.description}" class="w-12 h-12" />
                    <span class="sr-only">{payment_method.description}</span>
                </div>
            """

        return {
            "data": [
                {
                    "title": "Het betaalproces",
                    "id": "payment",
                    "text": (
                        "Ons betaalproces is ontworpen om zo eenvoudig mogelijk te zijn.<br><br>"
                        "<ol class='list-decimal list-inside space-y-4'>"
                        "<li>U plaatst uw order via onze website door de gewenste producten aan uw winkelmand toe te voegen en uw gegevens in te vullen. "
                        "Tijdens het plaatsen van uw order kunt u ook een gewenste afleverdatum aangeven.</li>"
                        "<li>Na het aanmaken van uw order kiest u een betaalmethode zoals <strong>iDEAL</strong>, <strong>creditcard</strong>, of <strong>PayPal</strong> om uw betaling veilig te voltooien.</li>"
                        "<li>Zodra uw betaling succesvol is verwerkt, wordt uw gekozen afleverdatum doorgegeven aan onze bezorgservice. Zij nemen contact met u op om te bevestigen of deze datum geschikt is, en indien nodig stemmen zij een alternatieve datum af die beter bij u past.</li>"
                        "<li>Wanneer uw bestelling is geleverd, wordt uw order voltooid in onze webshop. Hierna is het voor u mogelijk, indien noodzakelijk, een <a href='/return-service' class='font-medium text-orange-500'> retournering</a> aan te maken voor de betreffende producten.</li>"
                        "</ol><br>"
                        "Wij zorgen ervoor dat het proces soepel verloopt en dat u altijd op de hoogte bent van de status van uw bestelling."
                    ),
                },
                {
                    "title": "Beschikbare betaalmethoden",
                    "text": (
                        "Bij ons kunt u kiezen uit diverse veilige en gemakkelijke betaalmethoden, waaronder:<br><br>"
                        "<ul class='list-disc list-inside space-y-2'>"
                        "<li><strong>iDEAL:</strong> Betaal direct via uw eigen bank.</li>"
                        "<li><strong>Creditcard:</strong> Wij accepteren Visa en Mastercard.</li>"
                        "<li><strong>PayPal:</strong> Betaal eenvoudig met uw PayPal-account.</li>"
                        "</ul><br>"
                        "Met deze opties kunt u op de manier betalen die het beste bij u past, zonder extra zorgen."
                    ),
                    "additional_data": payments_html
                },
                {
                    "title": "De verzendkosten",
                    "text": (
                        "Wij hanteren transparante verzendkosten zodat u precies weet waar u aan toe bent:<br><br>"
                        "<ul class='list-disc list-inside space-y-2'>"
                        "<li><strong>Gratis verzending:</strong> Bij bestellingen boven de <strong>€500</strong> zijn de verzendkosten gratis.</li>"
                        "<li><strong>Verzendkosten:</strong> Voor bestellingen onder de <strong>€500</strong> rekenen wij een vaste bijdrage van <strong>€50</strong>.</li>"
                        "</ul><br>"
                        "Onze bezorgservice zorgt ervoor dat uw bestelling op een veilige en professionele manier wordt afgeleverd."
                    )
                },
                {
                    "title": "Onze bezorgservice",
                    "id": "delivery",

                    "text": (
                        "Zodra uw order is betaald, nemen wij het van daaruit over. Onze bezorgservice neemt de door u gekozen afleverdatum in behandeling en stemt met u hierbij het gewenste tijdstip af. "
                        "Indien nodig nemen zij contact met u op om een alternatieve datum af te stemmen.<br><br>"
                        "Wij leveren uw bestelling normaal gesproken binnen <strong>96 uur</strong> op werkdagen, overal in <strong>Nederland</strong> en <strong>België</strong>.<br><br>"
                        "Wij begrijpen hoe belangrijk het is om uw bestelling op tijd en in perfecte staat te ontvangen, en daarom besteden wij extra aandacht aan elk detail. Echter zou het altijd kunnen door bepaalde factoren dat dit uit kan lopen. Wij informeren u hier spoedig over.<br><br>"
                        "Heeft u speciale verzoeken of vragen over de levering? Neem gerust <a href='/contact-service' class='font-medium text-orange-500'>contact met ons op</a>, wij staan klaar om u te helpen."
                    ),
                }
            ],
            "extra": "Alles wat u moet weten over betaling en levering",
            "name": "Betaling & verzending",
            "header": "Uw bestelling, onze zorg!",
            "description": (
                "Wij willen het bestellen en ontvangen van uw vloeren zo eenvoudig en zorgeloos mogelijk maken.<br><br>"
                "Tijdens het plaatsen van uw bestelling kunt u een gewenste afleverdatum opgeven. Wij geven deze door aan onze <a class='font-medium text-orange-500' href='#delivery'>bezorgservice</a>, die vervolgens contact met u opneemt om de levering te bevestigen en de details af te stemmen. "
                "Voor de betaling bieden wij verschillende veilige opties, zoals <strong>iDEAL</strong>, <strong>creditcard</strong> en <strong>PayPal</strong>. "
                "Uw bestelling wordt pas verwerkt nadat de betaling is voltooid.<br><br>"
                "Bij bestellingen vanaf <strong>€500</strong> nemen wij de verzendkosten voor onze rekening. Voor bestellingen onder dit bedrag rekenen wij een vaste bijdrage van <strong>€50</strong>. "
                "Wij streven ernaar uw bestelling binnen <strong>96 uur</strong> op werkdagen te leveren en bezorgen in <strong>Nederland</strong> en <strong>België</strong>. "
                "Onze bezorgservice doet er alles aan om uw bestelling op tijd en in perfecte staat af te leveren.<br><br>"
                "Hoewel we zorgvuldig te werk gaan, kunnen er soms onvoorziene omstandigheden zijn die invloed hebben op de levertijd. Mocht dit het geval zijn, dan brengen we u hier tijdig van op de hoogte. <br><br>"
                "<strong>Heeft u vragen over deze procedure?</strong> Neem gerust <a href='/contact-service' class='font-medium text-orange-500'>contact met ons op</a>!"
            ),
        }
