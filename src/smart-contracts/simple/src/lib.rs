#![no_std]

imports!();

/// One of the simplest smart contracts possible,
/// it holds a single variable in storage, which anyone can increment.
#[elrond_wasm_derive::contract(AdderImpl)]
pub trait Adder {
	
	#[view(getSum)]
	#[storage_get("sum")]
	fn get_sum(&self) -> BigInt;

	#[storage_set("sum")]
	fn set_sum(&self, sum: &BigInt);

	#[init]
	fn init(&self, initial_value: &BigInt) {
		self.set_sum(initial_value);
	}

	/// Add desired amount to the storage variable.
	#[endpoint]
	fn add(&self, value: &BigInt) -> SCResult<()> {
		let mut sum = self.get_sum();
		sum += value;
		self.set_sum(&sum);

		Ok(())
	}

	#[endpoint]
	fn register_visit(&self, caller: &Address) -> SCResult<()> {
		let origin = self.get_caller(); /// We need the transaction origin here but no idea of how to do it
		self.register_visit_event(&caller, &origin);
		Ok(())
	}

	#[event("0x0000000000000000000000000000000000000000000000000000000000000001")]
	fn register_visit_event(&self, #[indexed] contract_address: &Address, #[indexed] caller_wallet: &Address);
}
