import React from 'react';
import Layout from 'Layouts';
import Row from "@paljs/ui/Row";
import Col from "@paljs/ui/Col";
import {Card, CardBody} from "@paljs/ui/Card";
//import {loadStripe} from "@stripe/stripe-js/pure";
//import {Elements, useElements, useStripe} from "@stripe/react-stripe-js";
//import axios from "axios";

//const stripePromise = loadStripe('pk_test_CuwDopxPO5sBVADCFCPV5XO900f5T2YEBL');


/*const CheckOutForm = () => {
    const [error, setError] = useState(null);
    const stripe = useStripe();
    const elements = useElements();
// Handle real-time validation errors from the CardElement.
    const handleChange = (event: any) => {
        if (event.error) {
            setError(event.error.message);
        } else {
            setError(null);
        }
    }
// Handle form submission.
    const handleSubmit = async (event: any) => {
        try {
            event.preventDefault();
            // @ts-ignore
            /!*const card = elements.getElement(CardElement);

            // add these lines
            // @ts-ignore
            const {paymentMethod, error} = await stripe.createPaymentMethod({
                type: 'card',
                // @ts-ignore
                card: card
            });

            console.log(paymentMethod)*!/


            const response = await axios.post("http://localhost:8000/api/payments/", {
                    // @ts-ignore
                    //payment_method_id: paymentMethod.id,
                    order_id: "59302211-845e-4864-8a20-53b13f8ccc11"
                },
                {
                    headers: {
                        Authorization: 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI1NTM0NjcwLCJqdGkiOiI5MzQxZjNhMDBhNjI0ZDJjOTRhYTU5ODc1YmRjZjdlOCIsInVzZXJfaWQiOjN9.ZnVQ5YVcKeYopWnqsjBPfEnb2bv6qc9kP9utXSGLW-k',
                        "Content-type": "application/json"
                    }
                })

            console.log(response, error)
        } catch (e) {
            console.log(e);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="stripe-form">
            {/!*<div className="form-row">
                <label form="card-element">Credit or debit card</label>
                <CardElement id="card-element" onChange={handleChange}/>
                <div className="card-errors" role="alert">{error}</div>
            </div>*!/}
            <button type="submit" className="submit-btn">
                Submit Payment
            </button>
        </form>
    )
}*/

const Home = () => {


    return (
        <Layout title="Home">
            <Row>
                <Col breakPoint={{xs: 12, md: 6}}>
                    <Card>
                        <header>Testowa płatnosc kartą</header>
                        <CardBody>
                            1
                        </CardBody>
                    </Card>
                </Col>
            </Row>
        </Layout>
    );
};
export default Home;
