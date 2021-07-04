import React, {useState} from 'react';
import Layout from 'Layouts';
import Row from "@paljs/ui/Row";
import Col from "@paljs/ui/Col";
import {Card, CardBody} from "@paljs/ui/Card";
import {loadStripe} from "@stripe/stripe-js/pure";
import {CardElement, Elements, useElements, useStripe} from "@stripe/react-stripe-js";
import axios from "axios";

const stripePromise = loadStripe('pk_test_CuwDopxPO5sBVADCFCPV5XO900f5T2YEBL');


const CheckOutForm = () => {
	const [error, setError] = useState(null);
	const [email, setEmail] = useState('');
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
		event.preventDefault();
		// @ts-ignore
		const card = elements.getElement(CardElement);

		// add these lines
		// @ts-ignore
		const {paymentMethod, error} = await stripe.createPaymentMethod({
			type: 'card',
			// @ts-ignore
			card: card
		});

		const response = await axios.post("http://localhost:8000/api/payments/", {
			payment_method_id: paymentMethod
		})

		console.log(response, error)
	};

	return (
		<form onSubmit={handleSubmit} className="stripe-form">
			<div className="form-row">
				<label htmlFor="email">Email Address</label>
				<input className="form-input" id="email" name="name" type="email"
					   placeholder="jenny.rosen@example.com" required
					   value={email} onChange={(event) => {
					setEmail(event.target.value)
				}}/>
			</div>
			<div className="form-row">
				<label form="card-element">Credit or debit card</label>
				<CardElement id="card-element" onChange={handleChange}/>
				<div className="card-errors" role="alert">{error}</div>
			</div>
			<button type="submit" className="submit-btn">
				Submit Payment
			</button>
		</form>
	)
}

const Home = () => {


	return (
		<Layout title="Home">
			<Row>
				<Col breakPoint={{xs: 12, md: 6}}>
					<Card>
						<header>Testowa płatnosc kartą</header>
						<CardBody>
							<Elements stripe={stripePromise}>
								<CheckOutForm />
							</Elements>
						</CardBody>
					</Card>
				</Col>
			</Row>
		</Layout>
	);
};
export default Home;
