package game

type Game struct {
	suspicion    int
	comfort      int
	currentID    string
	proceduralN  int
	tree         map[string]*Node
}

type Node struct {
	ID       string
	Dialogue string
	Choices  []Choice
}

type Choice struct {
	Text      string
	NextID    string
	SuspDelta int
	ComfDelta int
}

func New() *Game {
	g := &Game{
		suspicion:   3,
		comfort:     3,
		currentID:   "start",
		proceduralN: 0,
		tree:        buildTree(),
	}
	return g
}

func (g *Game) CurrentNode() *Node {
	node, ok := g.tree[g.currentID]
	if !ok {
		return nil
	}
	return g.resolveNode(node)
}

func (g *Game) MakeChoice(idx int) {
	resolved := g.CurrentNode()
	if resolved == nil || idx < 0 || idx >= len(resolved.Choices) {
		return
	}

	choice := resolved.Choices[idx]
	g.suspicion += choice.SuspDelta
	g.comfort += choice.ComfDelta

	if g.suspicion < 0 {
		g.suspicion = 0
	}
	if g.suspicion > 10 {
		g.suspicion = 10
	}
	if g.comfort < 0 {
		g.comfort = 0
	}
	if g.comfort > 10 {
		g.comfort = 10
	}

	if g.suspicion >= 10 {
		g.currentID = "hangup"
		return
	}

	if isProceduralChoice(choice.NextID) {
		g.proceduralN++
	}

	g.currentID = choice.NextID
}

func isProceduralChoice(nextID string) bool {
	switch nextID {
	case "b2_procedure", "b3_email", "b3_name", "b3_check_account",
		"b4_verify_email", "b4_verify_name", "b4_options",
		"b5_security_q", "b5_recovery_opts", "b6_hint_prompt",
		"b6_hint_think", "b7_hint_recall":
		return true
	}
	return false
}

func (g *Game) resolveNode(node *Node) *Node {
	switch node.ID {
	case "a4_pet_ask":
		if g.comfort >= 7 && g.suspicion <= 4 {
			return g.tree["a4_pet_real"]
		}
		if g.suspicion >= 7 {
			return g.tree["a4_pet_fake"]
		}
		return g.tree["a4_pet_vague"]
	case "a5_year_ask":
		if g.comfort >= 5 && g.suspicion <= 5 {
			return g.tree["a5_year_real"]
		}
		return g.tree["a5_year_deflect"]
	case "b7_hint_recall":
		if g.suspicion <= 3 && g.proceduralN >= 3 {
			return g.tree["b7_hint_real"]
		}
		return g.tree["b7_hint_fail"]
	}
	return node
}
