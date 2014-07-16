
rh.dwf.DiceRoundController = function() {
	this.diceRound = new rh.dwf.DiceRound();
	this.$score = $("#round-score");
	this.$offTableButtons = $(".dice-row.off-table button");
	this.$onTableButtons = $(".dice-row.on-table button");
	this.$rollButton = $("#btn-roll-again");
	this.$stopButton = $("#btn-stop");
	this.enableButtons();
	this.updateAll();
};

rh.dwf.DiceRoundController.prototype.enableButtons = function() {
	diceRoundController = this;
	$(".dice-row button").click(function() {
		idComponents = this.id.split("-");
		die = diceRoundController.diceRound.pressedButtonAtLocation(idComponents[3], idComponents[1] == "on");
		diceRoundController.updateDie(die);
		// Update the view for other dice that might have moved.
		for (var i = 0; i < die.otherLocationsToMoveOffTable.length; ++i) {
			dependentDieLocation = die.otherLocationsToMoveOffTable[i];
			dependentDie = diceRoundController.diceRound.getDieAtLocation(dependentDieLocation);
			diceRoundController.updateDie(dependentDie);
		}
		diceRoundController.updateButtonActionStates();
		diceRoundController.updateScore();
	});
	$("#btn-roll-again").click(function() {
		hasActiveDice = diceRoundController.diceRound.roll();
		diceRoundController.updateAll();
		if (!hasActiveDice) {
			// TODO: Animate losing all your points
		}
	});
//	$("#btn-stop").click(function() {
//		diceRoundController.diceRound = new rh.dwf.DiceRound();
//		diceRoundController.updateAll();
//	});
};


rh.dwf.DiceRoundController.prototype.updateAll = function () {
	for (var i = 0; i < 6; ++i) {
		this.updateDie(this.diceRound.getDieAtLocation(i));
	}
	this.updateButtonActionStates();
	this.updateScore();
};


rh.dwf.DiceRoundController.prototype.updateButtonActionStates = function() {
	if (this.diceRound.isRoundOver()) {
		this.$rollButton.prop('disabled', true);
		this.$stopButton.prop('disabled', false);
		this.$stopButton.html("Next Turn");
	} else {
		if (this.diceRound.hasRemovedAnActiveDie()) {
			this.$rollButton.prop('disabled', false);
		} else {
			this.$rollButton.prop('disabled', true);
		}
		this.$stopButton.html("Stop");
		if (this.diceRound.getRoundScore() > 0) {
			this.$stopButton.prop('disabled', false);
		} else {
			this.$stopButton.prop('disabled', true);
		}
	}
};


rh.dwf.DiceRoundController.prototype.updateScore = function() {
	if (this.diceRound.isRoundOver()) {
		this.$score.html("BUST!");
	} else {
		this.$score.html(this.diceRound.getRoundScore());
	}
	$("input[name='new_score']").val(this.diceRound.getRoundScore()); // TODO: Refactor
};


rh.dwf.DiceRoundController.prototype.updateDie = function (die) {
	switch (die.state) {
	case rh.dwf.Die.ACTIVE_ON_TABLE:
		$(this.$offTableButtons[die.location]).html("");
		$(this.$onTableButtons[die.location]).html(die.value);
		break;
	case rh.dwf.Die.ACTIVE_OFF_TABLE:
		$(this.$offTableButtons[die.location]).html(die.value);
		$(this.$onTableButtons[die.location]).html("");
		break;
	case rh.dwf.Die.INACTIVE_ON_TABLE:
		$(this.$offTableButtons[die.location]).html("");
		$(this.$onTableButtons[die.location]).html(die.value + ".");
		break;
	case rh.dwf.Die.INACTIVE_OFF_TABLE:
		$(this.$offTableButtons[die.location]).html("x");
		$(this.$onTableButtons[die.location]).html("");
		break;
	}
};