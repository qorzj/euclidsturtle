from euclidsturtle.geotool import Line, Segment, get_axialsymmetry_point


def test_get_axialsymmetry_point():
    # Create a line for axis of symmetry
    axis_segment = Segment(1, 1, 3, 3)
    axis = Line(axis_segment)
    print(f'axis: {axis.a}x + {axis.b}y = {axis.c}')

    # Test a point that is symmetric to the axis
    p1 = (2, 2)
    symmetric_point1 = get_axialsymmetry_point(p1, axis)
    assert symmetric_point1 == (2, 2)

    # Test a point that is not symmetric to the axis
    p2 = (4, 1)
    symmetric_point2 = get_axialsymmetry_point(p2, axis)
    assert symmetric_point2 == (1, 4)

    # Another axis that is not aligned with the previous one
    axis_segment = Segment(1, 1, 3, 2)
    axis = Line(axis_segment)
    print(f'axis: {axis.a}x + {axis.b}y = {axis.c}')

    # Test with a point on the axis itself
    p3 = (2, 1.5)
    symmetric_point3 = get_axialsymmetry_point(p3, axis)
    assert symmetric_point3 == (2, 1.5)

    # Test with a point off the axis
    p4 = (3, 3)
    symmetric_point4 = get_axialsymmetry_point(p4, axis)
    axis_segment_for_check = Segment(*p4, *symmetric_point4)
    assert symmetric_point4 == (3.8, 1.4)

    # Test more points
    p5 = (0, 0)
    symmetric_point5 = get_axialsymmetry_point(p5, axis)
    assert symmetric_point5 == (-0.4, 0.8)

    # Another axis that is not aligned with the previous one
    axis_segment = Segment(4, 5.3, 4, 2)
    axis = Line(axis_segment)

    p6 = (1, 2)
    symmetric_point6 = get_axialsymmetry_point(p6, axis)
    assert symmetric_point6 == (7, 2)

    # Another axis that is not aligned with the previous one
    axis_segment = Segment(4, 5.3, 6.6, 5.3)
    axis = Line(axis_segment)

    p7 = (2.5, 0)
    symmetric_point7 = get_axialsymmetry_point(p7, axis)
    assert symmetric_point7 == (2.5, 10.6)
